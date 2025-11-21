import os
from typing import Annotated

from fastapi import HTTPException, Header
from fastapi.params import Depends
from starlette import status

API_KEY = os.getenv("API_KEY")


async def verify_api_key(x_api_key: Annotated[str, Header()]):
    """
    Dependency для проверки API ключа
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return x_api_key

ApiKeyDep = Annotated[str, Depends(verify_api_key)]
