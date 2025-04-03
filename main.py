from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from hxc import process_query
import json
from typing import Optional

app = FastAPI(title="HXC API")

class QueryRequest(BaseModel):
    education: str
    graduation_years: int
    query: str

@app.post("/api/query")
async def stream_query(request: QueryRequest):
    async def generate():
        try:
            # 调用process_query函数
            response = process_query(
                education=request.education,
                graduation_years=request.graduation_years,
                query=request.query,
                stream=True
            )
            
            # 将响应分块发送
            for chunk in response.content:
                yield f"data: {json.dumps({'content': chunk})}\n\n"
                
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

from typing import List
from datetime import datetime

class UserInfo(BaseModel):
    user_id: str
    is_online: bool
    gender: str
    education: str
    age: int
    province: str
    city: str
    district: str
    chat_count: int
    last_active: datetime

# 模拟用户数据存储
users_db = [
    {
        "user_id": "u001",
        "is_online": True,
        "gender": "男",
        "education": "本科",
        "age": 28,
        "province": "广东省",
        "city": "深圳市", 
        "district": "南山区",
        "chat_count": 15,
    },
    {
        "user_id": "u002",
        "is_online": False,
        "gender": "女",
        "education": "硕士",
        "age": 25,
        "province": "北京市",
        "city": "海淀区",
        "district": "中关村",
        "chat_count": 10,
    }
]

@app.get("/api/users", response_model=List[UserInfo])
async def get_users():
    """获取所有用户信息"""
    try:
        return users_db
    except Exception as e:
        return {"error": str(e)}











if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 