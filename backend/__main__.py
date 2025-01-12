from fastapi import FastAPI

from backend import handlers

app = FastAPI()

app.include_router(handlers.router)


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host="0.0.0.0",
        port=80
    )
