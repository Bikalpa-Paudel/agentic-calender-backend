from src.db.models import User
from sqlalchemy.orm import Session, defer
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, name: str, email: str, password: str) -> User:
        try:
            user = User(name=name, email=email, password=password)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user

        except IntegrityError as e:
            self.db.rollback()
            raise e

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

        except Exception as e:
            self.db.rollback()
            raise e 


    def get_user_by_email(self, email:str):
        try:
            user = self.db.query(User).filter_by(email=email).first()
            return user
        
        except IntegrityError as e:
            self.db.rollback()
            raise e

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

        except Exception as e:
            self.db.rollback()
            raise e
    

    def get_user_by_id(self, id:str):
        try:
            return self.db.query(User).options(defer(User.password)).filter_by(id=id).first()

        except IntegrityError as e:
            self.db.rollback()
            raise e

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

        except Exception as e:
            self.db.rollback()
            raise e

