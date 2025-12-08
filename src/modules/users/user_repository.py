from src.db.models import User
from sqlalchemy.orm import Session

class UserRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, name:str, email:str):
        user = User(name=name, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_list(self):
        return self.db.query(User).all()