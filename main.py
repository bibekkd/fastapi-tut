from fastapi import FastAPI
from blog import models
from blog.database import engine
from blog.routers.blogs import router as blog_router
from blog.routers.users import router as user_router
from blog.routers.auth import router as auth_router

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)



# Include routers
app.include_router(blog_router)
app.include_router(user_router)
app.include_router(auth_router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)
    