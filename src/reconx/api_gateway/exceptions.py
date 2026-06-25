from typing import Any, Dict, Optional, List

class ReconXException(Exception):
    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR", status_code: int = 500, details: Optional[List[Dict[str, Any]]] = None):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or []
        super().__init__(self.message)

class ValidationException(ReconXException):
    def __init__(self, message: str = "Validation failed", details: Optional[List[Dict[str, Any]]] = None):
        super().__init__(message, error_code="VALIDATION_ERROR", status_code=422, details=details)

class AuthenticationException(ReconXException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, error_code="AUTHENTICATION_ERROR", status_code=401)

class AuthorizationException(ReconXException):
    def __init__(self, message: str = "Authorization failed"):
        super().__init__(message, error_code="AUTHORIZATION_ERROR", status_code=403)

class TenantException(ReconXException):
    def __init__(self, message: str = "Tenant isolation violation"):
        super().__init__(message, error_code="TENANT_ERROR", status_code=403)

class RateLimitException(ReconXException):
    def __init__(self, message: str = "Too many requests"):
        super().__init__(message, error_code="RATE_LIMIT_ERROR", status_code=429)

class ResourceNotFoundException(ReconXException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, error_code="NOT_FOUND", status_code=404)

class ConflictException(ReconXException):
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, error_code="CONFLICT", status_code=409)

def setup_exception_handlers(app):
    from fastapi import Request
    from fastapi.responses import JSONResponse
    from reconx.api_gateway.responses import ErrorResponse, ErrorDetail
    from fastapi.exceptions import RequestValidationError
    import logging
    
    logger = logging.getLogger(__name__)
    
    @app.exception_handler(ReconXException)
    async def reconx_exception_handler(request: Request, exc: ReconXException):
        details = [ErrorDetail(field=d.get("field"), message=d.get("message", str(d))) for d in exc.details]
        error_response = ErrorResponse(
            error_code=exc.error_code,
            message=exc.message,
            details=details
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump()
        )
        
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        details = []
        for error in exc.errors():
            loc = ".".join(str(l) for l in error.get("loc", []))
            details.append(ErrorDetail(field=loc, message=error.get("msg", "Invalid field")))
            
        error_response = ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="Request validation failed",
            details=details
        )
        return JSONResponse(
            status_code=422,
            content=error_response.model_dump()
        )
        
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled exception processing {request.method} {request.url}")
        error_response = ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred."
        )
        return JSONResponse(
            status_code=500,
            content=error_response.model_dump()
        )
