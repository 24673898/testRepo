import os
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.api.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.user import TokenData, UserResponse
from app.services.auth_service import get_or_create_user
from app.utils.db import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

def _keycloak_base() -> str:
    return (os.getenv("OIDC_ISSUER") or "").replace("/realms/penflow", "")

def _get_admin_token() -> str:
    admin_username = os.getenv("KEYCLOAK_ADMIN_USERNAME")
    admin_password = os.getenv("KEYCLOAK_ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        raise RuntimeError("CRITICAL: Keycloak admin credentials are not set in the environment.")

    res = httpx.post(
        f"{_keycloak_base()}/realms/master/protocol/openid-connect/token",
        data={
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": admin_username,
            "password": admin_password,
        },
    )
    res.raise_for_status()
    token: str = res.json()["access_token"]
    return token


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, db: Session = Depends(get_db)) -> UserResponse:
    try:
        admin_token = _get_admin_token()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Keycloak unreachable",
        ) from exc

    res = httpx.post(
        f"{_keycloak_base()}/admin/realms/penflow/users",
        headers={
            "Authorization": f"Bearer {admin_token}",
            "Content-Type": "application/json",
        },
        json={
            "username": body.username,
            "email": body.email,
            "enabled": True,
            "emailVerified": True,
            "credentials": [
                {"type": "password", "value": body.password, "temporary": False}
            ],
        },
    )

    if res.status_code == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        )
    if res.status_code != 201:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to create user in Keycloak",
        )

    location = res.headers.get("Location", "")
    keycloak_user_id = location.rstrip("/").split("/")[-1]

    token_data = TokenData(sub=keycloak_user_id, email=body.email, name=body.username)
    user = get_or_create_user(db, token_data, provider="keycloak")
    return UserResponse.model_validate(user)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)
