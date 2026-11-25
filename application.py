from fastapi import FastAPI

from database import models, engine
from api.routes import auth, posts, reaction


def create_app(db_engine=engine):
    models.Base.metadata.create_all(bind=db_engine)
    app = FastAPI()
    app.include_router(auth.router, prefix="/auth")
    app.include_router(posts.router, prefix="/piazza_posts")
    app.include_router(reaction.router, prefix="/piazza_posts")
    @app.get("/")
    def home():
        return {"message": "Welcome to the Piazza Project"}

    return app