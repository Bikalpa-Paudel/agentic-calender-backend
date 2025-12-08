from fastapi import APIRouter, Depends
from src.db.session import get_db
from .user_schema import UserResponse, UserCreate
from .user_service import UserService
from .user_repository import UserRepository
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model= list[UserResponse])
def get_user_list( db:Session = Depends(get_db)):
     service = UserService(UserRepository(db))
     return service.list_user()

@router.post("/", response_model=UserResponse)
def create_user(body : UserCreate, db: Session = Depends(get_db)):
     service = UserService(UserRepository(db))
     return service.create_user(name = body.name, email= body.email)

