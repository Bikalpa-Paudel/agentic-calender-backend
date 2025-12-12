from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.utils.password_utils import hash_password, verify_password
from src.utils.jwt_utils import create_jwt_token

class UserService:

    def __init__(self, repo):
        self.repo = repo
        
    def create_user(self, name: str, email: str, password: str):
        hashed = hash_password(password)

        try:
            user = self.repo.create_user(name=name, email=email, password=hashed)
            token = create_jwt_token({"id": user.id})
            return {"access_token": token, "user": user}

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email already exists"
            )

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Database operation failed"
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Unexpected server error: {str(e)}"
            )


    def login_user(self, email:str, password:str):
        user = self.repo.get_user_by_email(email)
    
        invalid_credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
        if not user:
            raise invalid_credentials_exception
            
        if not verify_password(plain_password=password, hashed_password=user.password):
            raise invalid_credentials_exception

        token = create_jwt_token({"id": user.id})
        return {"access_token": token, "token_type": "bearer"}
    
    def get_user_by_id(self, id:str):
        return self.repo.get_user_by_id(id)