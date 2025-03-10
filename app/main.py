from dotenv import load_dotenv
from app.routes import book_router, user_router, borrowing_router, auth_router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import CustomHTTPException
from core.rate_limiting import apply_rate_limiting

load_dotenv()
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
