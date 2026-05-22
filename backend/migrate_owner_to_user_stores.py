"""
迁移脚本：将 stores.owner_id 同步到 user_stores 表
"""
import asyncio
import sys
sys.path.insert(0, r"C:\Users\adminisator\Desktop\zc\backend")

from uuid import UUID
from sqlalchemy import select

from app.core.database import async_session_factory
from app.models.store import Store
from app.models.user import UserStore


async def migrate():
    async with async_session_factory() as db:
        # 查所有有 owner_id 的门店
        result = await db.execute(
            select(Store).where(Store.owner_id.isnot(None))
        )
        stores = list(result.scalars().all())
        print(f"找到 {len(stores)} 个有 owner_id 的门店")

        added = 0
        for store in stores:
            # 检查 user_stores 是否已有记录
            existing = await db.execute(
                select(UserStore).where(
                    UserStore.user_id == store.owner_id,
                    UserStore.store_id == store.id,
                )
            )
            if not existing.scalar_one_or_none():
                db.add(UserStore(user_id=store.owner_id, store_id=store.id))
                added += 1
                print(f"  添加关联: user={store.owner_id}, store={store.name}")

        await db.commit()
        print(f"✅ 迁移完成，新增 {added} 条 user_stores 记录")


if __name__ == "__main__":
    asyncio.run(migrate())
