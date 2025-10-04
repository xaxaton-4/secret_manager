import logging

from core import app
from fastapi import Depends
from models.auth import User
from services.auth import get_current_user


logger = logging.getLogger('secret_manager')


@app.get('/users/me/', response_model=User)
async def _users_me(user: User = Depends(get_current_user)) -> User:
    """Return current authorized user"""
    return user
