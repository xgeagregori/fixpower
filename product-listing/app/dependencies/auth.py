from fastapi import HTTPException, status, Depends

from fastapi.security import OAuth2PasswordBearer

import os
import requests

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def check_user_is_admin(current_user):
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
        )


def check_user_permissions(current_user, user_id: int):
    if current_user["id"] != user_id and not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
        )


# Dependency to get access token from header and verify it
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_response = requests.get(
        os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    if user_response.status_code != 200:
        raise credentials_exception

    return user_response.json()
