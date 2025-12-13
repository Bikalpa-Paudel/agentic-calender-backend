from fastapi import APIRouter, Depends, Form
from src.db.session import get_db
from .user_schema import UserResponse, UserCreate, UserLogin
from .user_service import UserService
from .user_repository import UserRepository
from sqlalchemy.orm import Session
from src.middleware.auth_middleware import auth_middleware_validation

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/login")
def login_user(body: UserLogin = Form(...), db=Depends(get_db)):
    return UserService(UserRepository(db)).login_user(email=body.username, password=body.password)
@router.get("/", response_model= list[UserResponse])
def get_user_list( db:Session = Depends(get_db)):
     service = UserService(UserRepository(db))
     return service.list_user()

@router.post("/")
def create_user(body: UserCreate, db=Depends(get_db)):
    service = UserService(UserRepository(db))
    response = service.create_user(name=body.name, email=body.email, password=body.password)
    return response

@router.post("/google/init")
def google_init(redirect_uri = str, db=Depends(get_db)):
    return UserService(UserRepository(db)).google_auth_init(redirect_uri)

@router.post("/google")
async def google_auth(code:str, db=Depends(get_db)):
    service =  UserService(UserRepository(db))
    response = service.google_login(code=code)
    return response


@router.get("/me", response_model=UserResponse)
def get_me(db=Depends(get_db), current_user: UserResponse = Depends(auth_middleware_validation)):
    return UserService(UserRepository(db)).get_user_by_id(current_user.id)