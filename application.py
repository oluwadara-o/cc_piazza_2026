from fastapi import FastAPI

def create_app():
    app = FastAPI()

    @app.get("/")
    def home():
        return {"message": "Welcome to the Piazza Project"}

    return app