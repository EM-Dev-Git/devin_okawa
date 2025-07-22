from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.modules.auth import verify_token
from src.modules.user_store import user_store
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token_data = verify_token(token, credentials_exception)
        user = user_store.get_user_by_username(token_data.username)
        
        if user is None:
            logger.warning(f"User not found for token: {token_data.username}")
            raise credentials_exception
        
        if not user.get("is_active", False):
            logger.warning(f"Inactive user attempted access: {token_data.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}")
        raise credentials_exception
