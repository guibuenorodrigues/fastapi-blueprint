from fastapi import APIRouter

router = APIRouter(prefix="/healthz", tags=["Health"])


@router.get("")
async def healthz():
    return {}
