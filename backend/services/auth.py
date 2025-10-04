import logging
from time import time
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from models.auth import TokenData, User, UserInDB
from passlib.context import CryptContext

from core import oauth2_scheme
from constants.errors import AuthError, TokenError
from config import settings


logger = logging.getLogger('secret_manager')


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_users_in_db() -> None:
    for username, user in {}:
        if user.get('hashed'):
            # Protect from double hashing
            continue

        user["hashed_password"] = hash_password(user["hashed_password"])
        user["hashed"] = True


hash_users_in_db()


def get_user(username: str) -> Optional[UserInDB]:
    user_dict = {}
    if user_dict is None:
        return None

    return UserInDB(**user_dict)


def authenticate_user(username: str, password: str) -> User:
    user = get_user(username)
    if not user:
        raise AuthError('User not found')

    if not verify_password(password, user.hashed_password):
        raise AuthError('Incorrect password')

    return user


def create_access_token(user: User, expires_delta: Optional[int] = None) -> str:
    if expires_delta is None:
        expires_delta: int = settings.DEFAULT_TOKEN_EXPIRATION_TIME

    expire = time() + expires_delta
    payload = {"exp": expire, "sub": user.login, "name": user.displayed_name}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def parse_and_validate_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError as e:
        raise TokenError(f"Invalid token: {str(e)}") from e

    username: Optional[str] = payload.get("sub")
    if username is None:
        raise TokenError("No username in token")

    expiration_time: Optional[int] = payload.get("exp")
    if expiration_time is None:
        raise TokenError("No expiration time in token")

    return TokenData(username=username)


def refresh_access_token(refresh_token: str) -> str:
    token_data = parse_and_validate_token(refresh_token)

    user = get_user(token_data.username)
    if user is None:
        raise AuthError("User not found")

    token = create_access_token(user)
    return token


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        token_data = parse_and_validate_token(token)
    except TokenError as e:
        logger.warning('Could not validate credentials: %s', e)
        raise credentials_exception

    user = get_user(token_data.username)
    if user is None:
        logger.warning('Could not validate credentials: user not found')
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user
