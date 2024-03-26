from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import Union, Dict, Optional

class Books(BaseModel):
    id: int 
    title:str
    author: str | None = None
    description: str | None = None
    published_year: int | None = None

    # 데이터 검증
    @validator('published_year')
    def yearcheck(cls, v):
        if v > 2024:
            raise ValueError('publisehd_year는 현재보다 미래일 수 없습니다.')

app = FastAPI()
FakeDB: Dict[int, Books] = {}

# 도서 추가
@app.post("/books")
async def newbooks(books: Books):
    if FakeDB[books.id]:
        raise HTTPException(status_code = 400, detail = "이미 존재하는 도서입니다.")
    else:
        FakeDB[books.id] = books
        raise HTTPException(status_code = 201, detail = '성공적으로 추가되었습니다')

# 모든 도서 목록 반환
@app.get("/books")
async def allbooks():
    return FakeDB

# 도서 검색 
@app.get("/books/search")
async def searchbooks(title: Optional[str] = None, author: Optional[str] = None, published_year: Optional[int] = None):
    searched_books = []
    for book in FakeDB.values():
        if title and title not in book.title:
            continue
        if author and author not in book.author:
            continue
        if published_year and published_year != book.published_year:
            continue
        searched_books.append(book)
    if not searched_books:
        raise HTTPException(status_code = 404, detail = "요청하신 도서를 찾을 수 없습니다.")
    return searched_books

# 특정 도서 조회
@app.get("/books/{id}")
async def readbooks(id: int):
    if not FakeDB[id]:
        raise HTTPException(status_code = 404, detail = "요청하신 ID와 일치하는 도서를 찾을 수 없습니다.")
    return FakeDB[id]

# 특정 도서 정보 업데이트
@app.put("/books/{id}")
async def updatebooks(id:int, books: Books):
    if id not in FakeDB:
        raise HTTPException(status_code = 404, detail = "해당하는 도서를 찾을 수 없습니다.")
    FakeDB[id] = books
    raise HTTPException(status_code = 201, detail = "성공적으로 변경되었습니다." )

# 특정 도서 삭제
@app.delete("/books/{id}")
async def deletebooks(id: int):
    if id not in FakeDB:
        raise HTTPException(status_code = 404, detail = "해당하는 도서를 찾을 수 없습니다.")
    del FakeDB[id]
    raise HTTPException(status_code = 201, detail = "성공적으로 삭제되었습니다.")
