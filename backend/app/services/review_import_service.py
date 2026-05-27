"""
评论导入导出服务
支持从 Excel/CSV 文件批量导入评论数据，以及导出评论到 Excel
"""

from __future__ import annotations

import io
import tempfile
import uuid
from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pandas import DataFrame, read_csv, read_excel

from app.core.exceptions import BusinessException
from app.models.review import Review


# 支持的字段映射（中文列名 -> 英文字段名）
COLUMN_MAPPING = {
    # 中文列名
    "评论内容": "content",
    "内容": "content",
    "评论": "content",
    "评分": "rating",
    "星级": "rating",
    "平台": "platform",
    "来源": "platform",
    "平台评论ID": "platform_review_id",
    "评论者": "user_name",
    "昵称": "user_name",
    "头像": "user_avatar",
    "图片": "images",
    "图片链接": "images",
    "回复": "reply",
    "商家回复": "reply",
    "回复时间": "replied_at",
    "创建时间": "created_at",
    # 英文列名（直接映射）
    "content": "content",
    "rating": "rating",
    "platform": "platform",
    "platform_review_id": "platform_review_id",
    "user_name": "user_name",
    "user_avatar": "user_avatar",
    "images": "images",
    "reply": "reply",
    "replied_at": "replied_at",
    "created_at": "created_at",
}

# 必填字段
REQUIRED_COLUMNS = ["content"]

# 可选字段及其类型验证
OPTIONAL_COLUMNS = {
    "rating": (float, int),
    "platform": str,
    "images": str,
    "reply": str,
    "replied_at": str,
    "created_at": str,
}


async def import_reviews_from_file(
    db: AsyncSession,
    file: UploadFile,
    store_id: str,
) -> dict:
    """
    从上传的 Excel/CSV 文件批量导入评论
    
    Args:
        db: 数据库会话
        file: 上传的文件对象
        store_id: 店铺ID（所有评论关联到这个店铺）
        current_user_id: 当前用户ID（作为评论的 user_id）
        
    Returns:
        dict: {success_count: 成功数量, skip_count: 跳过数量, errors: 错误列表, warning: 警告信息}
        
    Raises:
        BusinessException: 文件格式错误、字段不兼容等
    """
    # 1. 验证文件
    if not file or not file.filename:
        raise BusinessException("请上传有效的文件")
    
    filename = file.filename.lower()
    if not (filename.endswith(".xlsx") or filename.endswith(".csv")):
        raise BusinessException("只支持 .xlsx 或 .csv 文件，当前文件格式不支持")
    
    # 2. 读取文件内容
    try:
        content = await file.read()
        if not content:
            raise BusinessException("上传的文件为空")
    except Exception as e:
        raise BusinessException(f"读取文件失败：{str(e)}")
    
    # 3. 解析文件
    try:
        if filename.endswith(".xlsx"):
            df = _parse_excel(content)
        elif filename.endswith(".csv"):
            df = _parse_csv(content)
        else:
            raise BusinessException("不支持的文件格式")
    except BusinessException:
        raise
    except Exception as e:
        raise BusinessException(f"文件解析失败：{str(e)}")
    
    # 4. 验证数据是否为空
    if df.empty:
        raise BusinessException("上传的文件没有数据，请检查文件内容")
    
    # 5. 标准化列名（支持中英文）
    try:
        df = _normalize_columns(df)
    except Exception as e:
        raise BusinessException(f"列名标准化失败：{str(e)}")
    
    # 6. 验证必填列
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        available_cols = "、".join(df.columns.tolist())
        raise BusinessException(
            f"缺少必填列：{', '.join(missing_cols)}\n"
            f"提示：文件必须包含「评论内容」或「content」列\n"
            f"当前文件包含的列：{available_cols}\n\n"
            f"【支持的字段】\n"
            f"必填：评论内容(content)\n"
            f"可选：评分(rating, 数字1-5)、平台(platform, 如meituan/dianping)、"
            f"图片(images, 逗号分隔的URL)、回复(reply)、回复时间(replied_at)、创建时间(created_at)\n\n"
            f"【模板下载】请联系管理员获取导入模板"
        )
    
    # 7. 批量插入
    success_count = 0
    skip_count = 0
    errors = []
    warnings = []
    
    for idx, row in df.iterrows():
        try:
            # 验证并提取内容（必填）
            content_val = _extract_string_value(row, "content")
            if not content_val:
                skip_count += 1
                errors.append(f"第 {idx+2} 行：评论内容为空，已跳过")
                continue
            
            # 验证并提取评分（可选，默认5）
            rating_val = _extract_rating_value(row, "rating", errors, idx)
            
            # 验证并提取平台（可选，默认meituan）
            platform_val = _extract_string_value(row, "platform", default="meituan")
            if platform_val and platform_val not in ["meituan", "dianping", "other"]:
                warnings.append(f"第 {idx+2} 行：平台「{platform_val}」未知，已自动设置为「other」")
                platform_val = "other"
            
            # 验证并提取平台评论ID（可选，导入时自动生成）
            platform_review_id_val = _extract_string_value(row, "platform_review_id")
            if not platform_review_id_val:
                platform_review_id_val = f"import_{uuid.uuid4()}"

            # 验证并提取评论者昵称（可选，从文件读取）
            user_name_val = _extract_string_value(row, "user_name")
            
            # 验证并提取图片（可选）
            images_val = _extract_string_value(row, "images")
            if images_val:
                images_val = [url.strip() for url in images_val.split(",") if url.strip()]
            
            # 验证并提取回复（可选）
            reply_val = _extract_string_value(row, "reply")
            
            # 验证并提取回复时间（可选）
            replied_at_val = _extract_string_value(row, "replied_at")
            reply_time_val = None
            if replied_at_val:
                try:
                    reply_time_val = datetime.fromisoformat(replied_at_val.replace("Z", "+00:00"))
                except Exception:
                    pass
            
            # 验证并提取创建时间（可选）
            created_at_val = _extract_string_value(row, "created_at")
            platform_created_at_val = None
            if created_at_val:
                try:
                    platform_created_at_val = datetime.fromisoformat(created_at_val.replace("Z", "+00:00"))
                except Exception:
                    pass
            
            # 构造 Review 对象（只使用模型有的字段）
            review = Review(
                store_id=store_id,
                platform=platform_val or "meituan",
                platform_review_id=platform_review_id_val,
                rating=rating_val,
                content=content_val,
                user_name=user_name_val,          # 评论者昵称（可选）
                images=images_val,                # JSON 数组
                reply=reply_val,                  # 商家回复
                reply_time=reply_time_val,        # 回复时间（datetime）
                platform_created_at=platform_created_at_val,  # 平台创建时间
            )
            
            db.add(review)
            success_count += 1
            
            # 每 100 条提交一次
            if success_count % 100 == 0:
                await db.commit()
        
        except Exception as e:
            error_msg = f"第 {idx+2} 行：{str(e)}"
            errors.append(error_msg)
            skip_count += 1
    
    # 最终提交
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise BusinessException(f"数据库提交失败：{str(e)}")
    
    result = {
        "success_count": success_count,
        "skip_count": skip_count,
        "errors": errors[:20],  # 只返回前 20 个错误
        "total": len(df),
    }
    
    if warnings:
        result["warnings"] = warnings[:10]  # 只返回前 10 个警告
    
    return result


def export_reviews_to_excel(
    reviews: list[dict],
    filename: str = "评论导出.xlsx",
) -> io.BytesIO:
    """
    将评论数据导出为 Excel 文件
    
    Args:
        reviews: 评论数据列表
        filename: 文件名（仅用于标识）
        
    Returns:
        io.BytesIO: Excel 文件流
    """
    # 转换为 DataFrame
    df = DataFrame(reviews)
    
    # 重新排列列顺序（友好展示）
    columns_order = [
        "id", "store_id", "platform", "rating", "content",
        "images", "reply", "replied_at", "created_at",
    ]
    # 只保留存在的列
    columns_exist = [c for c in columns_order if c in df.columns]
    df = df[columns_exist]
    
    # 写入 Excel
    output = io.BytesIO()
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        df.to_excel(tmp.name, index=False, engine="openpyxl")
        tmp.seek(0)
        output.write(tmp.read())
    
    output.seek(0)
    return output


def generate_import_template(include_example: bool = False) -> io.BytesIO:
    """
    生成导入模板 Excel 文件
    
    Args:
        include_example: 是否包含示例数据，默认 False（只有表头）
        
    Returns:
        io.BytesIO: 模板文件流
    """
    if include_example:
        # 带示例数据的模板
        template_data = {
            "评论内容": [
                "这家店的服务态度很好，菜品也很新鲜",
                "环境不错，但上菜速度有点慢",
                "性价比很高，会再来",
            ],
            "评分": [5, 3, 4],
            "平台": ["meituan", "dianping", "meituan"],
            "平台评论ID": ["mt_001", "dp_002", ""],
            "评论者": ["张三", "李四", "王五"],
            "图片": [
                "https://example.com/img1.jpg,https://example.com/img2.jpg",
                "",
                "https://example.com/img3.jpg",
            ],
            "回复": [
                "感谢您的好评！",
                "非常抱歉给您带来不好的体验，我们会改进",
                "",
            ],
        }
    else:
        # 空白模板（只有表头）
        template_data = {
            "评论内容": [],
            "评分": [],
            "平台": [],
            "平台评论ID": [],
            "评论者": [],
            "图片": [],
            "回复": [],
        }
    
    df = DataFrame(template_data)
    
    output = io.BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)
    
    return output


def _parse_excel(content: bytes) -> DataFrame:
    """解析 Excel 文件"""
    try:
        df = read_excel(io.BytesIO(content), engine="openpyxl")
        return df
    except Exception as e:
        raise BusinessException(f"Excel 解析失败：{str(e)}\n提示：请确保文件是有效的 .xlsx 格式")


def _parse_csv(content: bytes) -> DataFrame:
    """解析 CSV 文件"""
    try:
        # 尝试 UTF-8，失败后尝试 GBK
        try:
            df = read_csv(io.BytesIO(content), encoding="utf-8")
        except UnicodeDecodeError:
            df = read_csv(io.BytesIO(content), encoding="gbk")
        return df
    except Exception as e:
        raise BusinessException(f"CSV 解析失败：{str(e)}\n提示：请确保文件编码是 UTF-8 或 GBK")


def _normalize_columns(df: DataFrame) -> DataFrame:
    """
    标准化列名（支持中英文映射）
    中文列名 -> 英文字段名
    """
    # 创建映射字典
    column_mapping = {}
    for col in df.columns:
        col_str = str(col).strip()
        if col_str in COLUMN_MAPPING:
            column_mapping[col] = COLUMN_MAPPING[col_str]
    
    # 重命名列
    if column_mapping:
        df = df.rename(columns=column_mapping)
    
    # 确保 content 列存在
    if "content" not in df.columns:
        # 尝试找到内容列
        for col in df.columns:
            if "内容" in str(col) or "content" in str(col).lower():
                df = df.rename(columns={col: "content"})
                break
    
    return df


def _extract_string_value(row, column: str, default: str = None) -> Optional[str]:
    """提取字符串值"""
    val = row.get(column)
    if val is None or (isinstance(val, float) and str(val) == "nan"):
        return default
    return str(val).strip() if val else default


def _extract_rating_value(row, column: str, errors: list, idx: int) -> float:
    """提取并验证评分值"""
    val = row.get(column)
    if val is None or (isinstance(val, float) and str(val) == "nan"):
        return 5.0  # 默认评分
    
    try:
        rating = float(val)
        if rating < 1 or rating > 5:
            errors.append(f"第 {idx+2} 行：评分 {rating} 超出范围(1-5)，已自动设置为 5")
            return 5.0
        return rating
    except (ValueError, TypeError):
        errors.append(f"第 {idx+2} 行：评分「{val}」格式错误，已自动设置为 5")
        return 5.0
