from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .routers.minutes import router as minutes_router
from .routers.auth import router as auth_router, login_router
from .modules.logger_config import setup_logger
from .middleware.auth import SessionAuthenticationMiddleware
from .config import settings
import logging

setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Meeting Minutes Generator",
    description="Azure OpenAI powered meeting minutes generation system with session-based authentication",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionAuthenticationMiddleware)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret_key,
    max_age=settings.session_expire_hours * 3600
)

app.include_router(login_router)
app.include_router(auth_router)
app.include_router(minutes_router)

@app.get("/")
async def root():
    return {"message": "Meeting Minutes Generator API", "status": "running", "auth": "required"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "meeting-minutes-generator"}

@app.get("/debug/routes")
async def debug_routes():
    """WSL環境デバッグ用: 登録されているルート一覧を表示"""
    routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append({
                "path": route.path,
                "methods": list(route.methods) if route.methods else [],
                "name": getattr(route, 'name', 'unnamed')
            })
    return {"routes": routes, "total_routes": len(routes)}

@app.get("/debug/network")
async def debug_network():
    """WSL環境デバッグ用: ネットワーク情報を表示"""
    import socket
    import os
    
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "unknown"
    
    return {
        "hostname": hostname,
        "local_ip": local_ip,
        "environment": "WSL" if "microsoft" in os.uname().release.lower() else "Linux",
        "platform": os.uname().sysname,
        "version": os.uname().release
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Meeting Minutes Generator API server with application-wide authentication")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
