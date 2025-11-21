# main.py
import asyncio

from fastapi import FastAPI

from app.api import init_app
from app.container import Container


def main() -> FastAPI:
    container = Container()

    db = container.db()

    fastapi_app = init_app(container.fastapi_app())

    @fastapi_app.on_event("startup")
    async def startup_event():
        await db.create_database()

    return fastapi_app


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:main', host='localhost', port=8000, reload=True)
