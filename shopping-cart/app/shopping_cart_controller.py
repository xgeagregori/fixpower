from fastapi import FastAPI

app = FastAPI()


@app.get("/shopping-carts")
async def root():
    return {"message": "Welcome to the Shopping Cart Service!"}