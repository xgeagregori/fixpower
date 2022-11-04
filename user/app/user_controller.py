from fastapi import FastAPI, Depends, HTTPException, status
from mangum import Mangum

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.dependencies.user import UserDep
from app.schemas.user import UserBase, UserCreate

app = FastAPI(
    root_path="/prod/user-api/v1",
    title="User API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/user-api/v1")
router = InferringRouter()


@cbv(router)
class UserController:
    @app.post("/login")
    async def login(
        form_data: OAuth2PasswordRequestForm = Depends(), self=Depends(UserDep)
    ):
        user = authenticate_user(
            self.user_service, form_data.username, form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

    @app.post("/register", status_code=status.HTTP_201_CREATED)
    def register(user: UserCreate, self=Depends(UserDep)):
        """Register user."""
        user_id = self.user_service.create_user(user)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User not created",
            )
        return {"id": user_id}

    @app.get("/users/me")
    def get_users(current_user: UserBase = Depends(get_current_user)):
        """Get authenticated user"""
        return current_user.attribute_values


app.include_router(router)
