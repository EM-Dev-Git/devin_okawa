from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db
from ..models import User
from ..schemas.auth import Token, UserRegister
from ..modules.auth import authenticate_user, create_access_token, get_password_hash
from ..modules.logger import get_logger
from ..config import settings

logger = get_logger(__name__)
router = APIRouter(prefix="/auth", tags=["認証"])


@router.post("/register", response_model=dict)
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    logger.info(f"ユーザー登録開始: {user.username}")
    
    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if db_user:
        logger.warning(f"ユーザー登録失敗 - 既存ユーザー: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ユーザー名またはメールアドレスが既に使用されています"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"ユーザー登録成功: {user.username}")
    return {"message": "ユーザー登録が完了しました", "user_id": db_user.id}


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"ログイン試行: {form_data.username}")
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"ログイン失敗: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"ログイン成功: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}
