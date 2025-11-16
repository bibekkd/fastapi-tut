from fastapi import FastAPI
from blog import models
from blog.database import engine
from blog.routes import router

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Include all routes
app.include_router(router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)
    