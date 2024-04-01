from fastapi import APIRouter
from api.v1.route_auth import router as auth_router

router = APIRouter()
router.include_router(router=auth_router)
