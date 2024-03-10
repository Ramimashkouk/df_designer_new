from fastapi import FastAPI, APIRouter
from app.api.api_v1.api import api_router

app = FastAPI(title="DF Designer")

root_router = APIRouter()


@root_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


app.include_router(root_router)
app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
