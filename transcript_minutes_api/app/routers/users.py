from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User
from ..schemas.users import User as UserSchema, UserUpdate
from ..dependencies import get_current_active_user
from ..modules.auth import get_password_hash
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/users", tags=["ユーザー管理"])


@router.get("/me", response_model=UserSchema)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    logger.info(f"ユーザー情報取得: {current_user.username}")
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"ユーザー情報更新開始: {current_user.username}")
    
    update_data = user_update.dict(exclude_unset=True)
    
    if "username" in update_data:
        existing_user = db.query(User).filter(
            User.username == update_data["username"],
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このユーザー名は既に使用されています"
            )
    
    if "email" in update_data:
        existing_user = db.query(User).filter(
            User.email == update_data["email"],
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このメールアドレスは既に使用されています"
            )
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"ユーザー情報更新完了: {current_user.username}")
    return current_user


@router.delete("/me")
async def delete_current_user(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"ユーザー削除開始: {current_user.username}")
    
    current_user.is_active = False
    db.commit()
    
    logger.info(f"ユーザー削除完了: {current_user.username}")
    return {"message": "ユーザーが正常に削除されました"}
