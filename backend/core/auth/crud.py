from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


async def get_user_by_email(
    session: AsyncSession,
    email: str
) -> Optional[User]:
    stmt = select(User).filter(User.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()
