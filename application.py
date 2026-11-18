from fastapi import FastAPI

from database import models, engine
from api.routes import auth


def create_app(db_engine=engine):
    models.Base.metadata.create_all(bind=db_engine)
    app = FastAPI()
    app.include_router(auth.router, prefix="/auth")
    @app.get("/")
    def home():
        return {"message": "Welcome to the Piazza Project"}

    return app