"""
评论路由模块
处理评论列表、详情、统计、回复等接口
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.response import paginated, success
from app.models.user import User
from app.schemas.review import (
    BatchDeleteRequest,
    QuickReplyRequest,
    ReviewCreateRequest,
    ReviewFilterParams,
    ReviewResponse,
    ReviewStatsResponse,
    ReviewUpdateRequest,
    SimilarReviewResponse,
)
from app.services import review_service


router = APIRouter(prefix="/reviews", tags=["评价管理"])


# ==================== 固定路径路由（必须放在 /{review_id} 之前）====================

@router.get("/import-template", summary="下载导入模板")
async def download_import_template(
    example: str = Query("false", description="是否包含示例数据 (true/false)"),
):
    """
    下载评论导入模板 Excel 文件
    - example=false（默认）：空白模板，只有表头
    - example=true：带示例数据的模板
    """
    from fastapi.responses import StreamingResponse
    from urllib.parse import quote

    from app.services.review_import_service import generate_import_template

    # 将字符串转为布尔值（支持 true/false、1/0、yes/no，不区分大小写）
    example_bool = example.lower() in ("true", "1", "yes", "on")

    output = generate_import_template(include_example=example_bool)

    # 文件名（ASCII 安全 + RFC 5987 UTF-8 编码）
    ascii_name = "import_template.xlsx"
    utf8_name = quote("评论导入模板（带示例）.xlsx" if example_bool else "评论导入模板（空白）.xlsx", safe="")
    headers = {
        "Content-Disposition": (
            f"attachment; filename={ascii_name}; "
            f"filename*=UTF-8''{utf8_name}"
        ),
    }

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )


@router.post("/import", summary="批量导入评论")
async def import_reviews(
    file: UploadFile,
    store_id: str = Query(..., description="关联店铺ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    从 Excel/CSV 文件批量导入评论
    - 支持 .xlsx 和 .csv 文件
    - 必填列：content（评论内容）
    - 可选列：platform, rating, images, reply
    """
    from app.services.review_import_service import import_reviews_from_file

    result = await import_reviews_from_file(
        db=db,
        file=file,
        store_id=store_id,
    )

    return success(
        data=result,
        message=f"导入完成：成功 {result['success_count']} 条，跳过 {result['skip_count']} 条",
    )


@router.get("/export", summary="导出评论")
async def export_reviews(
    sentiment: str | None = Query(None, description="情感筛选"),
    keyword: str | None = Query(None, description="关键词"),
    store_id: str | None = Query(None, description="店铺ID"),
    platform: str | None = Query(None, description="平台"),
    rating_min: int | None = Query(None, ge=1, le=5, description="最低评分"),
    rating_max: int | None = Query(None, ge=1, le=5, description="最高评分"),
    start_date: str | None = Query(None, description="开始日期"),
    end_date: str | None = Query(None, description="结束日期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    导出评论为 Excel 文件
    - 支持所有筛选条件
    - 返回 Excel 文件下载
    """
    from fastapi.responses import StreamingResponse
    from openpyxl import Workbook
    from io import BytesIO

    # 获取所有数据（不分页）
    filters = {
        "sentiment": sentiment,
        "keyword": keyword,
        "store_id": store_id,
        "platform": platform,
        "rating_min": rating_min,
        "rating_max": rating_max,
        "start_date": start_date,
        "end_date": end_date,
        "page": 1,
        "page_size": 10000,  # 导出大量数据
    }

    reviews, total = await review_service.get_reviews(db, current_user, filters)

    # 构造导出数据
    data = []
    for review in reviews:
        data.append({
            "ID": str(review.id),
            "店铺名称": review.store.name if review.store else "",
            "平台": review.platform,
            "评分": review.rating,
            "评论内容": review.content,
            "图片": ",".join(review.images) if review.images else "",
            "回复内容": review.reply or "",
            "回复时间": review.replied_at.strftime("%Y-%m-%d %H:%M:%S") if review.replied_at else "",
            "创建时间": review.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    # 生成 Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "评论数据"

    if data:
        # 写入表头
        headers = list(data[0].keys())
        ws.append(headers)

        # 写入数据
        for row in data:
            ws.append(list(row.values()))
    else:
        ws.append(["暂无数据"])

    # 返回文件流
    from urllib.parse import quote
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    # 文件名（ASCII 安全 + RFC 5987 UTF-8 编码）
    ascii_name = f"reviews_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    utf8_name = quote(f"评论导出_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx", safe="")
    headers = {
        "Content-Disposition": (
            f"attachment; filename={ascii_name}; "
            f"filename*=UTF-8''{utf8_name}"
        ),
    }

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )


# ==================== 普通路由 ====================

@router.get("", summary="评价列表")
async def get_reviews(
    sentiment: str | None = Query(None, description="情感: positive/negative/neutral"),
    keyword: str | None = Query(None, description="关键词搜索"),
    store_id: str | None = Query(None, description="门店ID"),
    platform: str | None = Query(None, description="来源平台"),
    rating_min: int | None = Query(None, ge=1, le=5, description="最低评分"),
    rating_max: int | None = Query(None, ge=1, le=5, description="最高评分"),
    has_reply: bool | None = Query(None, description="是否有回复"),
    has_image: bool | None = Query(None, description="是否有图片"),
    start_date: str | None = Query(None, description="开始日期(YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="结束日期(YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=500, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取评价列表
    - 支持按情感、平台、评分、关键词等条件筛选
    - 根据用户角色过滤可见评论
    """
    filters = {
        "sentiment": sentiment,
        "keyword": keyword,
        "store_id": store_id,
        "platform": platform,
        "rating_min": rating_min,
        "rating_max": rating_max,
        "has_reply": has_reply,
        "has_image": has_image,
        "start_date": start_date,
        "end_date": end_date,
        "page": page,
        "page_size": page_size,
    }

    reviews, total = await review_service.get_reviews(db, current_user, filters)

    items = []
    for review in reviews:
        review_data = ReviewResponse.model_validate(review).model_dump(mode="json")
        # 填充门店名称
        if review.store:
            review_data["store_name"] = review.store.name
        items.append(review_data)

    return paginated(items=items, total=total, page=page, page_size=page_size)


@router.get("/stats", summary="评价统计")
async def get_review_stats(
    period: str = Query("30d", description="统计周期: 7d/30d/90d/all"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取评价统计数据
    - 包含总数、情感分布、平均评分、回复率等
    """
    stats = await review_service.get_review_stats(db, current_user, period)

    return success(
        data=ReviewStatsResponse(**stats).model_dump(mode="json"),
    )


# ==================== 路径参数路由（必须放在最后）====================

@router.get("/{review_id}", summary="评价详情")
async def get_review_detail(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取评价详情
    """
    review = await review_service.get_review_by_id(db, review_id)

    review_data = ReviewResponse.model_validate(review).model_dump(mode="json")
    if review.store:
        review_data["store_name"] = review.store.name

    return success(data=review_data)


@router.get("/{review_id}/similar", summary="相似评论")
async def get_similar_reviews(
    review_id: UUID,
    limit: int = Query(5, ge=1, le=20, description="返回数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取相似评论列表
    - 基于相同门店和情感，按评分相近排序
    """
    reviews = await review_service.get_similar_reviews(db, review_id, limit)

    items = []
    for idx, review in enumerate(reviews):
        data = SimilarReviewResponse(
            id=review.id,
            user_name=review.user_name,
            content=review.content,
            rating=review.rating,
            sentiment=review.sentiment,
            similarity_score=round(1.0 - idx * 0.15, 2),  # 简化的相似度计算
        ).model_dump(mode="json")
        items.append(data)

    return success(data=items)


@router.post("", summary="新增评价")
async def create_review(
    request: ReviewCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    新增评价（爬虫入库用）
    """
    review = await review_service.create_review(db, request.model_dump())

    return success(
        data=ReviewResponse.model_validate(review).model_dump(mode="json"),
        message="评价创建成功",
    )


@router.put("/{review_id}", summary="更新评价")
async def update_review(
    review_id: UUID,
    request: ReviewUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    更新评价信息
    - 可更新回复内容和状态
    """
    review = await review_service.update_review(
        db, review_id, request.model_dump(exclude_none=True)
    )

    return success(
        data=ReviewResponse.model_validate(review).model_dump(mode="json"),
        message="评价更新成功",
    )


@router.delete("/{review_id}", summary="删除评价")
async def delete_review(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    删除评价（软删除）
    """
    await review_service.delete_review(db, review_id)

    return success(message="评价已删除")


@router.post("/batch-delete", summary="批量删除评价")
async def batch_delete_reviews(
    request: BatchDeleteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    批量删除评价（软删除）
    """
    count = await review_service.batch_delete_reviews(db, request.ids)

    return success(data={"deleted_count": count}, message=f"已删除 {count} 条评价")


@router.post("/{review_id}/like", summary="赞同评论")
async def like_review(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    赞同评论
    """
    review = await review_service.like_review(db, review_id)

    return success(message="操作成功")


@router.post("/{review_id}/reply", summary="快速回复")
async def quick_reply(
    review_id: UUID,
    request: QuickReplyRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    快速回复评论
    """
    review = await review_service.quick_reply(
        db, review_id, request.reply_content, current_user.id
    )

    return success(
        data=ReviewResponse.model_validate(review).model_dump(mode="json"),
        message="回复成功",
    )


@router.post("/{review_id}/approve-reply", summary="审核通过并发送回复")
async def approve_reply(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    审核通过 AI 回复并发送
    - 将 AI 回复草稿设为正式回复
    """
    audit = await review_service.approve_reply(db, review_id, current_user.id)

    return success(
        data={
            "id": str(audit.id),
            "status": audit.status,
            "reviewed_at": audit.reviewed_at.isoformat() if audit.reviewed_at else None,
        },
        message="回复已审核通过并发送",
    )
