from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def get_users():
    return {"message": "List of users"}

@router.post("/")
async def create_user(user: dict):
    return {"message": "User created", "user": user}

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"message": f"User with id {user_id}"}
