from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas.auth import Token, UserRegister
from ..schemas.users import UserResponse
from ..modules.auth import auth_service
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/auth", tags=["認証"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        logger.info(f"ユーザー登録開始: {user_data.username}")
        
        existing_user = db.query(User).filter(
            (User.username == user_data.username) | (User.email == user_data.email)
        ).first()
        
        if existing_user:
            logger.warning(f"ユーザー登録失敗: 既存ユーザー {user_data.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ユーザー名またはメールアドレスが既に使用されています"
            )
        
        hashed_password = auth_service.get_password_hash(user_data.password)
        
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"ユーザー登録成功: {user_data.username}")
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ユーザー登録エラー: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ユーザー登録に失敗しました"
        )


@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        logger.info(f"ログイン試行: {form_data.username}")
        
        user = db.query(User).filter(User.username == form_data.username).first()
        
        if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
            logger.warning(f"ログイン失敗: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ユーザー名またはパスワードが正しくありません",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            logger.warning(f"ログイン失敗: 無効なユーザー {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="無効なユーザーアカウントです"
            )
        
        access_token = auth_service.create_access_token(data={"sub": user.username})
        
        logger.info(f"ログイン成功: {form_data.username}")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ログインエラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ログインに失敗しました"
        )
