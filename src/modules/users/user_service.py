from .user_repository import UserRepository

class UserService():

    def __init__(self, repo:UserRepository):
        self.repo = repo
        
    def create_user(self, email:str, name: str):
        return self.repo.create_user(email=email, name=name)

    def list_user(self):
        return self.repo.get_user_list()