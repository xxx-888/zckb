"""
店铺名称相似度匹配工具

用于：
1. 不同平台店铺同步时，模糊匹配已有系统门店（避免重复创建）
2. Excel 周报导入时，模糊匹配 Excel 中的门店名到系统门店

匹配策略（三层递进）：
1. 标准化后完全一致 → 直接命中
2. 品牌+后缀分段匹配：品牌名相同 + 括号内后缀相似度高 → 命中
   例："犇犇...(綦江爱琴海店)" vs "犇犇...(綦江爱琴海公园店)" → 品牌"犇犇..."相同，后缀"綦江爱琴海店" vs "綦江爱琴海公园店"相似 → 同一门店
3. 全名 SequenceMatcher >= 阈值 → 命中
"""

import re
from difflib import SequenceMatcher
from typing import Optional, Tuple
from uuid import UUID


def normalize_store_name(name: str) -> str:
    """
    标准化店铺名称，消除不影响语义的差异

    处理规则：
    - 全角括号（）→ 半角括号 ()
    - 全角空格 → 半角空格
    - 去除首尾多余空格
    - 统一连续空格为单个空格
    """
    if not name:
        return ""
    s = name.strip()
    # 全角括号 → 半角
    s = s.replace("（", "(").replace("）", ")")
    # 全角空格 → 半角
    s = s.replace("\u3000", " ").replace("\u00a0", " ")
    # 统一连续空格
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _extract_brand_and_suffix(name: str) -> Tuple[str, str]:
    """
    将店铺名拆分为品牌名和后缀

    例：
    - "犇犇牛牛牛现切鲜牛肉烤串(微电园店)" → ("犇犇牛牛牛现切鲜牛肉烤串", "微电园店")
    - "犇犇牛牛牛现切鲜牛肉烤串（大学城店）" → ("犇犇牛牛牛现切鲜牛肉烤串", "大学城店")
    - "好火锅南坪店" → ("好火锅", "南坪店")
    """
    norm = normalize_store_name(name)
    if "(" in norm:
        # "品牌名(后缀)" 格式
        idx = norm.rfind("(")
        brand = norm[:idx].strip()
        suffix = norm[idx + 1:].rstrip(")").strip()
        return brand, suffix
    # 无括号，尝试提取末尾的 "XX店"
    if norm.endswith("店") and len(norm) > 2:
        # 简单启发：取最后一个"店"之前和之后的部分
        # 但中文店名复杂，不强制拆分，返回全名和空后缀
        return norm, ""
    return norm, ""


def _brand_suffix_similarity(name_a: str, name_b: str) -> float:
    """
    品牌+后缀分段相似度

    如果两个店名的品牌部分完全相同，且后缀部分也有一定相似度，
    则认为可能是同一门店。这样可以处理：
    - "XX(綦江爱琴海店)" vs "XX(綦江爱琴海公园店)" → 品牌100%匹配，后缀相似
    - "XX(大学城店)" vs "XX(甘孜店)" → 品牌100%匹配，但后缀不相似 → 不是同一门店
    """
    brand_a, suffix_a = _extract_brand_and_suffix(name_a)
    brand_b, suffix_b = _extract_brand_and_suffix(name_b)

    if not brand_a or not brand_b:
        return 0.0

    # 品牌必须完全一致
    if brand_a != brand_b:
        return 0.0

    # 品牌相同的情况下，比较后缀
    if not suffix_a and not suffix_b:
        return 1.0  # 都没有后缀，品牌相同 → 同一门店
    if not suffix_a or not suffix_b:
        return 0.5  # 一方有后缀一方没有，不确定

    # 后缀相似度
    suffix_sim = SequenceMatcher(None, suffix_a, suffix_b).ratio()

    return suffix_sim


def store_name_similarity(name_a: str, name_b: str) -> float:
    """
    计算两个店铺名称的综合相似度

    综合策略：
    - 标准化后完全一致 → 1.0
    - 包含匹配：短名称包含在长名称中 → 0.95（处理 Excel 简称 vs 系统全称）
    - 品牌+后缀分段匹配 → 直接使用后缀相似度
    - 全名 SequenceMatcher → 原始分数
    返回最高分数

    关键设计：品牌相同时，后缀相似度直接作为分数。
    这样"綦江爱琴海公园店"vs"綦江爱琴海店"→0.92（匹配），
    而"涪陵店"vs"奉节店"→0.33（不匹配）。
    """
    a = normalize_store_name(name_a)
    b = normalize_store_name(name_b)
    if not a or not b:
        return 0.0

    # 完全一致
    if a == b:
        return 1.0

    # 包含匹配：短名称被长名称包含 → 高相似度
    # 典型场景：Excel "大学城店" vs 系统 "犇犇牛牛牛现切鲜牛肉烤串(大学城店)"
    # 要求被包含方至少2个字符，避免单字误匹配
    shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
    if len(shorter) >= 2 and shorter in longer:
        return 0.95

    # 全名相似度
    full_sim = SequenceMatcher(None, a, b).ratio()

    # 品牌+后缀相似度（不映射到 [0.85, 1.0]，避免后缀差异大的店被误判为同一门店）
    brand_sim = _brand_suffix_similarity(name_a, name_b)
    if brand_sim > 0:
        return max(full_sim, brand_sim)

    return full_sim


def find_best_matching_store(
    query_name: str,
    store_name_map: dict[str, UUID],
    threshold: float = 0.9,
) -> tuple[Optional[UUID], float, str]:
    """
    在已有门店名称映射中找到与 query_name 最相似的门店

    匹配策略（三层递进）：
    1. 标准化后完全一致 → 直接命中 (score=1.0)
    2. 品牌+后缀分段匹配 ≥ 阈值 → 命中
    3. 全名 SequenceMatcher ≥ 阈值 → 命中
    """
    if not store_name_map:
        return None, 0.0, ""

    best_id = None
    best_score = 0.0
    best_name = ""

    query_normalized = normalize_store_name(query_name)

    for store_name, store_id in store_name_map.items():
        store_normalized = normalize_store_name(store_name)

        # 快速短路：标准化后完全一样
        if query_normalized == store_normalized:
            return store_id, 1.0, store_name

        # 综合相似度（含品牌+后缀分段策略）
        score = store_name_similarity(query_name, store_name)
        if score > best_score:
            best_score = score
            best_id = store_id
            best_name = store_name

    if best_score >= threshold:
        return best_id, best_score, best_name

    return None, 0.0, ""


def find_best_matching_store_from_list(
    query_name: str,
    store_list: list[dict],  # [{"id": UUID, "name": str}, ...]
    threshold: float = 0.9,
) -> tuple[Optional[UUID], float, str]:
    """
    从 ORM 查询结果列表中找最相似的门店

    与 find_best_matching_store 逻辑相同，输入格式不同
    """
    if not store_list:
        return None, 0.0, ""

    best_id = None
    best_score = 0.0
    best_name = ""

    query_normalized = normalize_store_name(query_name)

    for store in store_list:
        store_name = store.get("name", "")
        store_id = store.get("id")
        store_normalized = normalize_store_name(store_name)

        if query_normalized == store_normalized:
            return store_id, 1.0, store_name

        score = store_name_similarity(query_name, store_name)
        if score > best_score:
            best_score = score
            best_id = store_id
            best_name = store_name

    if best_score >= threshold:
        return best_id, best_score, best_name

    return None, 0.0, ""
