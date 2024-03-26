from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, validator
from typing import Union, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware

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

# 예외 클래스 - 도서가 없는 경우
class NoBookException(Exception):
    def __init__(self):
        self.message = '요청하신 도서를 찾을 수 없습니다.'
        super().__init__(self.message)

# 예외 클래스 - 도서가 이미 있는 경우
class ExistBookException(Exception):
    def __init__(self):
        self.message = '이미 존재하는 도서입니다.'
        super().__init__(self.message)

app = FastAPI()
FakeDB: Dict[int, Books] = {}

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# 도서 추가
@app.post("/books")
async def newbooks(books: Books):
    if FakeDB[books.id]:
        raise ExistBookException()
    else:
        FakeDB[books.id] = books
        raise HTTPException(status_code = 201, detail = '성공적으로 추가되었습니다.')

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
        raise NoBookException()
    return searched_books

# 특정 도서 조회
@app.get("/books/{id}")
async def readbooks(id: int):
    if not FakeDB[id]:
        raise NoBookException()
    return FakeDB[id]

# 특정 도서 정보 업데이트
@app.put("/books/{id}")
async def updatebooks(id:int, books: Books):
    if id not in FakeDB:
        raise NoBookException()
    FakeDB[id] = books
    raise HTTPException(status_code = 201, detail = "성공적으로 변경되었습니다." )

# 특정 도서 삭제
@app.delete("/books/{id}")
async def deletebooks(id: int):
    if id not in FakeDB:
        raise NoBookException()
    del FakeDB[id]
    raise HTTPException(status_code = 201, detail = "성공적으로 삭제되었습니다.")

# 예외 핸들러 - 도서가 없는 경우 
@app.exception_handler(NoBookException)
async def no_book_exception_handler(request: Request, exc: NoBookException):
    raise HTTPException(status_code = 404, detail = exc.message)

# 예외 핸들러 - 도서가 이미 있는 경우 
@app.exception_handler(ExistBookException)
async def exist_book_exception_handler(request: Request, exc: ExistBookException):
    raise HTTPException(status_code = 400, detail = exc.message)