from fastapi import APIRouter, HTTPException, Depends, status, Request, Form
from fastapi.responses import JSONResponse
from src.schemas.auth import UserCreate, UserResponse
from src.modules.auth import authenticate_user, register_user
import logging

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserResponse)
async def register_user_api(user_data: UserCreate):
    try:
        user = register_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        
        logger.info(f"User registration successful: {user_data.username}")
        return UserResponse(**user)
        
    except ValueError as e:
        logger.warning(f"User registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
async def login_user_api(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        user = authenticate_user(username, password)
        if not user:
            logger.warning(f"Failed login attempt: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        request.session["user_id"] = user['username']
        request.session["logged_in"] = True
        
        logger.info(f"User login successful: {username}")
        
        return JSONResponse(
            status_code=200,
            content={"message": "Login successful", "user": user['username']}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/logout")
async def logout_user(request: Request):
    user_id = request.session.get("user_id")
    if user_id:
        logger.info(f"User logout: {user_id}")
    
    request.session.clear()
    return JSONResponse(
        status_code=200,
        content={"message": "Logout successful"}
    )
