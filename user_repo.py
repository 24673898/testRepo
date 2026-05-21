from sqlalchemy.orm import Session

from app.models.user import User

#adjust the schema to the acutal db

def get_user_by_provider_id(db: Session, auth_provider: str, auth_provider_id: str) -> User | None:
    return (
        db.query(User)
        .filter(User.auth_provider == auth_provider, User.auth_provider_id == auth_provider_id)
        .first()
    )


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(
    db: Session,
    auth_provider: str,
    auth_provider_id: str,
    email: str,
    full_name: str | None = None,
) -> User:
    user = User(
        auth_provider=auth_provider,
        auth_provider_id=auth_provider_id,
        email=email,
        full_name=full_name,
        role="client",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
