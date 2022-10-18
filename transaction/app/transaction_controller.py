from fastapi import FastAPI

app = FastAPI()


@app.get("/transactions")
async def root():
    return {"message": "Welcome to the Transaction Service!"}