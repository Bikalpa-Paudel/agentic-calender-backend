from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.utils.password_utils import hash_password, verify_password
from src.utils.jwt_utils import create_jwt_token, decode_google_token
from src.core.config import settings
import httpx


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
    
    def google_auth_init(self, redirect_uri):
        return {
        "google_uri": (
            "https://accounts.google.com/o/oauth2/v2/auth"
             f"?client_id={settings.GOOGLE_CLIENT_ID}"
             f"&redirect_uri={redirect_uri}"
            "&response_type=code"
            "&scope=openid%20email%20profile%20https://www.googleapis.com/auth/calendar"
            "&access_type=offline"
            "&prompt=consent"
        )}
    
    def google_login(self, code:str):
        if not code:
            raise HTTPException(400, "Missing authorization code")

        token_url = "https://oauth2.googleapis.com/token"

        data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": "http://localhost:3000/auth/google/callback",
        "grant_type": "authorization_code",
        }


       
        token_response =  httpx.post(token_url, data=data)
    
        if token_response.status_code != 200:
            raise HTTPException(400, f"Token exchange failed: {token_response.text}")

        tokens = token_response.json()
        decoded_token = decode_google_token(tokens["id_token"])

        if(decoded_token):
            user = self.repo.get_user_by_email(decoded_token["email"])

            if(user):
                self.repo.update_tokens(user.id, access_token=tokens["access_token"], refresh_token=["refresh_token"])
                created_jwt = create_jwt_token({"id": user.id, "name": user.name, "email": user.email, "picture": user.picture})
                return {"access_token": created_jwt}
            
            else:
                created_user = self.repo.create_user(email=decoded_token["email"], name=decoded_token["name"], picture = decoded_token["picture"], access_token=tokens["access_token"], refresh_token=tokens["refresh_token"])
                created_jwt = create_jwt_token({"id": created_user.id, "name": created_user.name, "email": created_user.email, "picture": created_user.picture})
                return {"access_token": created_jwt}