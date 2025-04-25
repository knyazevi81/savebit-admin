from src.users.models import Users
from src.service.base import BaseService

class UserService(BaseService):
    model=Users
    
    
# await UserService.update({"login": "example_user"}, email="new_email@example.com")