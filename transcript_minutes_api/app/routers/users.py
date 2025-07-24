from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas.users import UserResponse, UserUpdate
from ..dependencies import get_current_active_user
from ..modules.auth import get_password_hash
from ..modules.logger import get_logger

router = APIRouter(prefix="/users", tags=["users"])
logger = get_logger(__name__)


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    logger.info(f"User profile accessed: {current_user.username}")
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"User profile update: {current_user.username}")
    
    if user_update.username is not None:
        existing_user = db.query(User).filter(
            User.username == user_update.username,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_user.username = user_update.username
    
    if user_update.email is not None:
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
        current_user.email = user_update.email
    
    if user_update.password is not None:
        current_user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"User profile updated successfully: {current_user.username}")
    return current_user


@router.delete("/me")
async def delete_user_me(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"User deletion: {current_user.username}")
    
    db.delete(current_user)
    db.commit()
    
    logger.info(f"User deleted successfully: {current_user.username}")
    return {"message": "User deleted successfully"}
