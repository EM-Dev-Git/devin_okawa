from fastapi import APIRouter, HTTPException, Depends, status, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from src.schemas.auth import UserCreate, UserResponse
from src.modules.auth import authenticate_user, register_user
import logging

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
logger = logging.getLogger(__name__)

login_router = APIRouter(tags=["authentication"])

@login_router.get("/login", response_class=HTMLResponse)
async def login_page():
    """Simple login page for browser access"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - Meeting Minutes Generator</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; }
            input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .error { color: red; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h2>Login to Meeting Minutes Generator</h2>
        <form action="/api/v1/auth/login" method="post">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <p><a href="/register">Don't have an account? Register here</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@login_router.get("/register", response_class=HTMLResponse)
async def register_page():
    """Simple registration page for browser access"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register - Meeting Minutes Generator</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; }
            input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            button { background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #1e7e34; }
            .error { color: red; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h2>Register for Meeting Minutes Generator</h2>
        <form id="registerForm">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Register</button>
        </form>
        <p><a href="/login">Already have an account? Login here</a></p>
        
        <script>
        document.getElementById('registerForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = {
                username: formData.get('username'),
                email: formData.get('email'),
                password: formData.get('password')
            };
            
            try {
                const response = await fetch('/api/v1/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    alert('Registration successful! Please login.');
                    window.location.href = '/login';
                } else {
                    const error = await response.json();
                    alert('Registration failed: ' + error.detail);
                }
            } catch (error) {
                alert('Registration failed: ' + error.message);
            }
        });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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
        
        content_type = request.headers.get("content-type", "")
        if "application/x-www-form-urlencoded" in content_type:
            from fastapi.responses import RedirectResponse
            return RedirectResponse(url="/", status_code=302)
        else:
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
