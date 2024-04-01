from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth.crud import get_user_by_email
from core.auth.utils import Hasher
from models.user import User


async def authenticate_user(
    session: AsyncSession,
    email: EmailStr,
    password: str,
) -> User | None:

    user = await get_user_by_email(session=session, email=email)
    if not user:
        return
    if not Hasher.validate_password(password, user.password):
        return
    return user
