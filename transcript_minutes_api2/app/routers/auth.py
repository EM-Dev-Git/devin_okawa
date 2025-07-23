from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.auth import UserLogin, Token
from ..modules.auth import auth_service
from ..models import User
from ..dependencies import get_current_user
from ..modules.logger import get_logger

router = APIRouter(prefix="/auth", tags=["認証"])
logger = get_logger(__name__)

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"ログイン試行: ユーザー {user_credentials.user_id}")
    
    user = db.query(User).filter(User.user_id == user_credentials.user_id).first()
    if not user:
        logger.warning(f"ログイン失敗: ユーザー {user_credentials.user_id} が見つかりません")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザーIDまたはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not auth_service.verify_password(user_credentials.password, user.password_hash):
        logger.warning(f"ログイン失敗: ユーザー {user_credentials.user_id} のパスワードが間違っています")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザーIDまたはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        logger.warning(f"ログイン失敗: ユーザー {user_credentials.user_id} は無効化されています")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="無効化されたユーザーです"
        )
    
    access_token = auth_service.create_access_token(data={"sub": user.user_id})
    logger.info(f"ログイン成功: ユーザー {user_credentials.user_id}")
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user)):
    logger.info(f"トークンリフレッシュ: ユーザー {current_user.user_id}")
    
    access_token = auth_service.create_access_token(data={"sub": current_user.user_id})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    logger.info(f"ログアウト: ユーザー {current_user.user_id}")
    
    return {"message": "正常にログアウトしました"}
