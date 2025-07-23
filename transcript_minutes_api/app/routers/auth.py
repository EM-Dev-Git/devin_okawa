from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..schemas.auth import Token, LoginRequest
from ..modules.auth import auth_service
from ..modules.logger import get_logger
from ..dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["認証"])
logger = get_logger(__name__)

@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    logger.info(f"ログイン試行: {login_data.user_id}")
    
    user = auth_service.authenticate_user(db, login_data.user_id, login_data.password)
    if not user:
        logger.warning(f"ログイン失敗: {login_data.user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザーIDまたはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth_service.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )
    
    logger.info(f"ログイン成功: {login_data.user_id}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user = Depends(get_current_user)
):
    access_token_expires = timedelta(minutes=auth_service.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": current_user.user_id}, expires_delta=access_token_expires
    )
    
    logger.info(f"トークンリフレッシュ: {current_user.user_id}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(current_user = Depends(get_current_user)):
    logger.info(f"ログアウト: {current_user.user_id}")
    return {"message": "ログアウトしました"}
