from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
def read_user_me():
    return {
        "id": "8eaae36f-01fc-434f-b19f-93754e0b87a8",
        "given_name": "John",
        "family_name": "Doe",
    }
