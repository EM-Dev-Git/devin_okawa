from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..config import settings
from .logger import get_logger

logger = get_logger(__name__)

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = settings.access_token_expire_minutes

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            result = self.pwd_context.verify(plain_password, hashed_password)
            logger.info(f"パスワード検証: {'成功' if result else '失敗'}")
            return result
        except Exception as e:
            logger.error(f"パスワード検証エラー: {str(e)}")
            return False

    def get_password_hash(self, password: str) -> str:
        try:
            hashed = self.pwd_context.hash(password)
            logger.info("パスワードハッシュ化成功")
            return hashed
        except Exception as e:
            logger.error(f"パスワードハッシュ化エラー: {str(e)}")
            raise

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        try:
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            
            logger.info(f"JWTトークン生成成功: ユーザー {data.get('sub')}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"JWTトークン生成エラー: {str(e)}")
            raise

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            logger.info(f"JWTトークン検証成功: ユーザー {payload.get('sub')}")
            return payload
        except JWTError as e:
            logger.error(f"JWTトークン検証エラー: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"トークン検証予期しないエラー: {str(e)}")
            raise

auth_service = AuthService()
