from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.modules.user_store import user_store
from src.config import settings
import logging

logger = logging.getLogger(__name__)

class SessionAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.excluded_paths = settings.excluded_paths_list
        logger.info(f"Session authentication middleware initialized with excluded paths: {self.excluded_paths}")

    async def dispatch(self, request: Request, call_next):
        logger.info(f"Processing request: {request.method} {request.url.path}")
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            logger.info(f"Path {request.url.path} is excluded from authentication - bypassing middleware")
            return await call_next(request)
        
        user_id = request.session.get("user_id")
        
        if not user_id:
            logger.warning(f"No session found for {request.url.path}")
            if request.url.path.startswith("/api/"):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Authentication required. Please login first."}
                )
            else:
                return RedirectResponse(url="/login", status_code=302)
        
        user = user_store.get_user_by_username(user_id)
        if not user:
            logger.warning(f"User {user_id} not found in store, clearing session")
            request.session.clear()
            if request.url.path.startswith("/api/"):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "User session invalid. Please login again."}
                )
            else:
                return RedirectResponse(url="/login", status_code=302)
        
        request.state.current_user = user_id
        logger.debug(f"Authenticated user: {user_id} for {request.url.path}")
        
        return await call_next(request)
