from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.users import UserCreate, UserResponse, UserUpdate
from ..modules.auth import auth_service
from ..models import User
from ..dependencies import get_current_user
from ..modules.logger import get_logger

router = APIRouter(prefix="/users", tags=["ユーザー管理"])
logger = get_logger(__name__)

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"ユーザー登録開始: {user.user_id}")
    
    db_user = db.query(User).filter(User.user_id == user.user_id).first()
    if db_user:
        logger.warning(f"ユーザー登録失敗: {user.user_id} は既に存在します")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このユーザーIDは既に登録されています"
        )
    
    if user.email:
        db_email = db.query(User).filter(User.email == user.email).first()
        if db_email:
            logger.warning(f"ユーザー登録失敗: メールアドレス {user.email} は既に使用されています")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このメールアドレスは既に使用されています"
            )
    
    hashed_password = auth_service.get_password_hash(user.password)
    
    db_user = User(
        user_id=user.user_id,
        password_hash=hashed_password,
        email=user.email
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"ユーザー登録成功: {user.user_id}")
    return db_user

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    logger.info(f"ユーザー情報取得: {current_user.user_id}")
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"ユーザー情報更新開始: {current_user.user_id}")
    
    if user_update.email:
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            logger.warning(f"ユーザー更新失敗: メールアドレス {user_update.email} は既に使用されています")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このメールアドレスは既に使用されています"
            )
        current_user.email = user_update.email
    
    if user_update.password:
        current_user.password_hash = auth_service.get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"ユーザー情報更新成功: {current_user.user_id}")
    return current_user
