from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union, Dict

class Books(BaseModel):
    id: int 
    title:str
    author: str | None = None
    description: str | None = None
    published_year: int | None = None

app = FastAPI()
FakeDB: Dict[int, Books] = {}

# 도서 추가
@app.post("/books")
async def newbooks(books: Books):
    FakeDB[books.id] = books
    return {f"{books.title}가 도서 목록에 추가되었습니다."}

# 모든 도서 목록 반환
@app.get("/books")
async def allbooks():
    return FakeDB

# 특정 도서 조회
@app.get("/books/{id}")
async def readbooks(id: int):
    return FakeDB[id]

# 특정 도서 정보 업데이트
@app.put("/books/{id}")
async def updatebooks(id:int, books: Books):
    FakeDB[id] = books
    return {f"{books.title}의 정보가 변경되었습니다."}

# 특정 도서 삭제
@app.delete("/books/{id}")
async def deletebooks(id: int):
    del FakeDB[id]
    return {"성공적으로 삭제되었습니다."}