from fastapi import FastAPI

app = FastAPI()


def get_message():
    return {"message": "Hello World"}


@app.get("/")
async def root():
    return get_message()
