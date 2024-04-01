from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm
from passlib.exc import UnknownHashError
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth.dependencies import get_current_user
from core.auth.schemas import Token
from core.auth.utils import Hasher, encode_jwt
from db.session import get_db_session
from models.user import User
from schemas.user import UserShow, UserCreate
from services.auth.utils import authenticate_user


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/me-info", response_model=UserShow)
async def get_user(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.post("/", response_model=UserShow, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_db_session),
):
    data = user.model_dump()
    data["password"] = Hasher.get_password_hash(data["password"])
    user = User(**data)
    session.add(user)
    await session.commit()
    return user


@router.post("/login/", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Login by specified email and password.
    :return: Access Token with user id, username and expire time.
    """
    http_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    try:
        user = await authenticate_user(session=session, email=form_data.username, password=form_data.password)
    except UnknownHashError:
        raise http_exc
    except Exception as ex:
        print(ex)
        raise http_exc
    if not user:
        raise http_exc
    jwt_payload = {
        "sub": user.email
    }
    access_jwt_token = encode_jwt(
        payload=jwt_payload
    )
    return Token(access_token=access_jwt_token, token_type="Bearer")

