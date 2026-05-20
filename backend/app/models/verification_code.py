"""
验证码模型
用于存储手机验证码（注册、忘记密码等场景）
"""

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import Boolean, DateTime, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class VerificationCode(Base):
    """验证码表模型"""
    
    __tablename__ = "verification_codes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(String(11), nullable=False, index=True, comment="手机号")
    code: Mapped[str] = mapped_column(String(6), nullable=False, comment="验证码")
    purpose: Mapped[str] = mapped_column(String(20), nullable=False, default="register", comment="用途：register/reset_password")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否已使用")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    def is_valid(self, input_code: str) -> bool:
        """检查验证码是否有效"""
        now = datetime.utcnow()
        return (
            not self.is_used
            and self.code == input_code
            and self.expires_at > now
        )
    
    @classmethod
    def generate_code(cls) -> str:
        """生成6位随机验证码"""
        import random
        return "".join([str(random.randint(0, 9)) for _ in range(6)])
    
    @classmethod
    def get_expiry_time(cls, minutes: int = 5) -> datetime:
        """获取过期时间"""
        return datetime.utcnow() + timedelta(minutes=minutes)
