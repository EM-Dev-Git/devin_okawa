from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
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
    
    if user_update.username and user_update.username != current_user.username:
        existing_user = db.query(User).filter(User.username == user_update.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このユーザー名は既に使用されています"
            )
        current_user.username = user_update.username
    
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このメールアドレスは既に使用されています"
            )
        current_user.email = user_update.email
    
    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)
    
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
