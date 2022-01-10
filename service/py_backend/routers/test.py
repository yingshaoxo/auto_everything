from fastapi import APIRouter

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/", tags=["test"])
async def testHomePage():
    return {"message": "Welcome to the test API"}


@router.get("/do", tags=["test"])
async def doIt():
    return {"message": "done"}
