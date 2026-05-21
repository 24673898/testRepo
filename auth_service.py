from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repo import create_user, get_user_by_provider_id
from app.schemas.user import TokenData


def get_or_create_user(db: Session, token_data: TokenData, provider: str = "keycloak") -> User:
    user = get_user_by_provider_id(db, provider, token_data.sub)
    if not user:
        user = create_user(
            db=db,
            auth_provider=provider,
            auth_provider_id=token_data.sub,
            email=token_data.email,
            full_name=token_data.name,
        )
    return user
