# 导入 SQLAlchemy 核心工具
from sqlalchemy import create_engine  # 用来创建数据库连接引擎
from sqlalchemy.ext.declarative import declarative_base  # 用来定义表的基类
from sqlalchemy.orm import sessionmaker  # 用来创建数据库会话（操作手柄）

# ===================== 1. 数据库文件路径 =====================
# SQLite 是文件型数据库
# sqlite:///./test.db 表示：在当前目录下创建 test.db 数据库文件
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# ===================== 2. 创建数据库引擎 =====================
# engine 是 Python 和 数据库之间的“桥梁”
# check_same_thread=False 是 SQLite 专用参数，必须加
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# ===================== 3. 创建会话工厂 =====================
# SessionLocal 是工厂，用来生产每个请求的“数据库连接会话”
# autocommit=False：不自动提交，必须手动 db.commit() 才会保存数据
# autoflush=False：不自动刷新
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ===================== 4. 声明基类 =====================
# 所有数据库表（模型）都必须继承 Base
# 它会自动把类映射成数据库表
Base = declarative_base()