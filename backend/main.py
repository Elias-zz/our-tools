# 导入 FastAPI 核心工具
from fastapi import FastAPI, Depends, HTTPException

# 导入数据库会话类型
from sqlalchemy.orm import Session

# ===================== 导入项目模块 =====================
# 数据库连接配置
from database import engine, SessionLocal, Base
# 数据库表模型（敏感词表）
from models import SensitiveWord
# 接口参数格式（创建、修改）
from schemas import SensitiveCreate, SensitiveUpdate

# ===================== 自动创建数据库和表 =====================
# 项目启动时自动根据 models.py 创建表和数据库文件 test.db
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用实例
app = FastAPI(title="敏感词过滤系统")

# ===================== 获取数据库连接 =====================
# 每次接口请求都会创建一个临时数据库连接
# 请求结束后自动关闭，防止资源泄漏
def get_db():
    # 创建数据库会话
    db = SessionLocal()
    try:
        # 把数据库连接交给接口使用
        yield db
    finally:
        # 无论请求是否成功，最后都关闭连接
        db.close()

# ===================== 接口 1：查询所有敏感词 =====================
@app.get("/sensitive/list")
def get_all_sensitive_words(db: Session = Depends(get_db)):
    """
    查询数据库中所有的敏感词
    """
    # 查询 sensitive_words 表所有数据
    words = db.query(SensitiveWord).all()

    return {
        "code": 200,
        "msg": "查询成功",
        "data": words
    }

# ===================== 接口 2：根据 ID 查询单个敏感词 =====================
@app.get("/sensitive/{word_id}")
def get_sensitive_word(word_id: int, db: Session = Depends(get_db)):
    """
    根据敏感词 ID 查询单条数据
    """
    # 根据 ID 查找敏感词
    word = db.query(SensitiveWord).filter(SensitiveWord.id == word_id).first()

    # 如果不存在，返回 404 错误
    if not word:
        raise HTTPException(status_code=404, detail="敏感词不存在")

    return {
        "code": 200,
        "msg": "查询成功",
        "data": word
    }

# ===================== 接口 3：添加敏感词 =====================
@app.post("/sensitive/add")
def add_sensitive_word(
    data: SensitiveCreate,
    db: Session = Depends(get_db)
):
    """
    添加新的敏感词（自动去重，不允许重复）
    """
    # 检查敏感词是否已经存在
    exists = db.query(SensitiveWord).filter(SensitiveWord.word == data.word).first()
    if exists:
        raise HTTPException(status_code=400, detail="该敏感词已存在")

    # 创建敏感词对象
    new_word = SensitiveWord(word=data.word)

    # 添加到数据库
    db.add(new_word)
    db.commit()
    db.refresh(new_word)

    return {
        "code": 200,
        "msg": "添加成功",
        "data": new_word
    }

# ===================== 接口 4：修改敏感词 =====================
@app.put("/sensitive/update/{word_id}")
def update_sensitive_word(
    word_id: int,
    data: SensitiveUpdate,
    db: Session = Depends(get_db)
):
    """
    根据 ID 修改敏感词内容
    """
    # 先查询要修改的敏感词
    word = db.query(SensitiveWord).filter(SensitiveWord.id == word_id).first()

    if not word:
        raise HTTPException(status_code=404, detail="敏感词不存在")

    # 更新内容
    word.word = data.word
    db.commit()
    db.refresh(word)

    return {
        "code": 200,
        "msg": "修改成功",
        "data": word
    }

# ===================== 接口 5：删除敏感词（根据 ID） =====================
@app.delete("/sensitive/delete/{word_id}")
def delete_sensitive_word(
    word_id: int,
    db: Session = Depends(get_db)
):
    """
    根据 ID 删除敏感词
    """
    # 查询要删除的敏感词
    word = db.query(SensitiveWord).filter(SensitiveWord.id == word_id).first()

    if not word:
        raise HTTPException(status_code=404, detail="敏感词不存在")

    # 执行删除
    db.delete(word)
    db.commit()

    return {
        "code": 200,
        "msg": "删除成功"
    }

# ===================== 项目启动：自动插入初始敏感词 =====================
@app.on_event("startup")
def init_sensitive_data():
    """
    项目启动时，如果表为空，自动插入默认敏感词
    """
    db = SessionLocal()
    try:
        # 统计表里有多少条数据
        count = db.query(SensitiveWord).count()

        # 如果表为空，插入初始数据
        if count == 0:
            print("✅ 正在初始化敏感词数据...")

            # 定义初始敏感词
            w1 = SensitiveWord(word="诈骗")
            w2 = SensitiveWord(word="赌博")
            w3 = SensitiveWord(word="毒品")

            # 批量添加
            db.add(w1)
            db.add(w2)
            db.add(w3)

            # 提交保存
            db.commit()

            print("✅ 初始敏感词插入完成！")

    finally:
        # 关闭数据库连接
        db.close()