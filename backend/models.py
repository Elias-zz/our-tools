# 导入字段类型（整数、字符串等）
from sqlalchemy import Column, Integer, String

# 从 database.py 导入表基类
from database import Base

# ===================== 敏感词表 =====================
class SensitiveWord(Base):
    # 数据库表名
    __tablename__ = "sensitive_words"

    # 主键 ID，自增
    id = Column(Integer, primary_key=True, index=True)
    # 敏感词
    word = Column(String, index=True)

# ===================== 变形词表 =====================
