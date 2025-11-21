from fastapi import APIRouter

from app.api.organisation import org_router


main_router = APIRouter(prefix='/api', tags=['API'])
main_router.include_router(org_router)
