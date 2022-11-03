from fastapi import FastAPI
from mangum import Mangum

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

app = FastAPI(
    root_path="/prod/user-api/v1",
    title="User API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/user-api/v1")
router = InferringRouter()


@cbv(router)
class UserController:
    @app.get("/users")
    def get_users():
        """Get users."""
        return {"message": "Welcome to the User Service!"}


app.include_router(router)
