from Library import app
from fastapi.testclient import TestClient

client = TestClient(app)

# 도서 추가 test
def test_newbooks():
    response = client.post("/books", json={
        "id": 1,
        "title": "testcase",
        "author": "Lee",
        "description": "Alright?",
        "published_year": 2024,
    })
    assert response.status_code == 201
    assert response.json() == {"detail": "성공적으로 추가되었습니다."}

# ExistBookException test - 도서 추가
def test_ExistBookException():
    response = client.post("/books", json={
        "id": 1,
        "title": "testcase",
        "author": "Lee",
        "description": "Alright?",
        "published_year": 2024,
    })
    assert response.status_code == 400
    assert response.json() == {"이미 존재하는 도서입니다."}

# 모든 도서 목록 반환 test
def test_allbooks():
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == {1: {"id": 1, "title": "testcase", "author": "Lee", "description": "Alright?", "published_year": 2024}}

# 도서 검색 test
def test_searchbooks():
    response = client.get("/books/search?id=1")
    assert response.status_code == 200
    assert response.json() == {1: {"id": 1, "title": "testcase", "author": "Lee", "description": "Alright?", "published_year": 2024}}

# NoBookException test - 도서 검색
def test_no_book_exception():
    response = client.get("/books/search?id=2")
    assert response.status_code == 404
    assert response.json() == "요청하신 도서를 찾을 수 없습니다."

# 특정 도서 조회 test
def test_readbooks():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {1: {"id": 1, "title": "testcase", "author": "Lee", "description": "Alright?", "published_year": 2024}}

# 특정 도서 정보 업데이트 test
def test_updatebooks():
    response = client.put("/books/1", json={
        "id": 1,
        "title": "testcase_2",
        "author": "Kim",
        "description": "Updated?",
        "published_year": 2024
    })
    assert response.status_code == 201
    assert response.json() == {"detail": "성공적으로 변경되었습니다."}

# 특정 도서 삭제 test
def test_deletebooks():
    response = client.delete("/books/1")
    assert response.status_code == 201
    assert response.json() == {"detail": "성공적으로 삭제되었습니다."}