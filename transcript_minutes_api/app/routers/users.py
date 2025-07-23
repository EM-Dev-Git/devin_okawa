from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from ..schemas.users import UserCreate, UserResponse, UserUpdate
from ..modules.auth import auth_service
from ..dependencies import get_current_user
from ..models import User
from ..modules.logger import get_logger

router = APIRouter(prefix="/users", tags=["ユーザー管理"])
logger = get_logger(__name__)

@router.post("/register", response_model=UserResponse)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    logger.info(f"ユーザー登録試行: {user.user_id}")
    
    existing_user = db.query(User).filter(User.user_id == user.user_id).first()
    if existing_user:
        logger.warning(f"ユーザー登録失敗 - 既存ユーザー: {user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このユーザーIDは既に使用されています"
        )
    
    try:
        db_user = auth_service.create_user(
            db=db,
            user_id=user.user_id,
            password=user.password,
            email=user.email
        )
        logger.info(f"ユーザー登録成功: {user.user_id}")
        return db_user
    except IntegrityError:
        logger.error(f"ユーザー登録失敗 - DB制約エラー: {user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ユーザー登録に失敗しました"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    logger.info(f"ユーザー情報取得: {current_user.user_id}")
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"ユーザー情報更新: {current_user.user_id}")
    
    if user_update.email is not None:
        current_user.email = user_update.email
    
    if user_update.password is not None:
        current_user.password_hash = auth_service.get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"ユーザー情報更新完了: {current_user.user_id}")
    return current_user
