from fastapi import FastAPI
from app.routes import book_router, user_router, borrowing_router, category_router, auth_router

app = FastAPI()

# Include routers
app.include_router(book_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(borrowing_router, prefix="/api")
app.include_router(category_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System!"}