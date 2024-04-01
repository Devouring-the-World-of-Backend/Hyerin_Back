from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_itmes():
    return {"Hello, Library!"}
