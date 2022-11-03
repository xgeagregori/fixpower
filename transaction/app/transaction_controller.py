from fastapi import FastAPI
from mangum import Mangum

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

app = FastAPI(
    root_path="/prod/transaction-api/v1",
    title="Transaction API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/transaction-api/v1")
router = InferringRouter()


@cbv(router)
class TransactionController:
    @app.get("/transactions")
    def get_transactions():
        """Get transactions."""
        return {"message": "Welcome to the Transaction Service!"}


app.include_router(router)
