from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import CustomHTTPException
from app.routes import auth_router
from app.routes import book_router
from app.routes import borrowing_router
from app.routes import user_router
from core.rate_limiting import apply_rate_limiting

app = FastAPI()

apply_rate_limiting(app)


@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail},
    )


app.include_router(book_router, prefix='/api')
app.include_router(user_router, prefix='/api')
app.include_router(borrowing_router, prefix='/api')
app.include_router(auth_router, prefix='/api')


@app.get('/')
def read_root():
    return {'message': 'Welcome to the Library Management System!'}
