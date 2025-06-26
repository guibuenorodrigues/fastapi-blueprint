from fastapi import APIRouter

router = APIRouter(prefix="/healthz", tags=["Health"])


@router.get("/")
def healthz():
    return {}
