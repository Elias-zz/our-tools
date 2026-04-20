
# 导入 pydantic 基类，用于参数校验
from pydantic import BaseModel, Field

# ===================== 1. 创建敏感词的参数格式 =====================
class SensitiveCreate(BaseModel):
    word: str = Field(..., min_length=1, max_length=50, description="敏感词内容")

# ===================== 2. 修改敏感词的参数格式 =====================
class SensitiveUpdate(BaseModel):
    word: str = Field(..., min_length=1, max_length=50, description="新的敏感词")

# ===================== 敏感词删除参数格式 =====================
class SensitiveDelete(BaseModel):
    id: int  # 只需要传敏感词ID

# ===================== 4. 敏感词返回格式 =====================
class SensitiveResponse(BaseModel):
    id: int
    word: str

    class Config:
        orm_mode = True  # 允许从数据库模型直接映射