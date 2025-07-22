from fastapi import Request, HTTPException, status
from typing import Optional

def get_current_user(request: Request) -> str:
    user_id = getattr(request.state, 'current_user', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user_id

def get_current_user_optional(request: Request) -> Optional[str]:
    return getattr(request.state, 'current_user', None)
