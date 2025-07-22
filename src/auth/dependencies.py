from fastapi import Depends, HTTPException, status
from .oauth2 import oauth2_scheme, verify_token
from src.modules.user_store import user_store
from .models import User

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token, credentials_exception)
    user = user_store.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return User(**{k: v for k, v in user.items() if k != 'hashed_password'})

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
