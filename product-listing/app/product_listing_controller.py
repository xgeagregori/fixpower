from fastapi import FastAPI

app = FastAPI()


@app.get("/product-listings")
async def root():
    return {"message": "Welcome to the Product Listings Service!"}
