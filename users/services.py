from __future__ import annotations
from typing import Any
from users.repositories import UserRepository
from users.selectors import UserSelector

class UserService:
    def __init__(self, repository: UserRepository | None = None, selector: UserSelector | None = None) -> None:
        self.repository = repository or UserRepository()
        self.selector = selector or UserSelector()

    def list_users(self):
        return self.selector.get_all()

    def get_user(self, user_id: str):
        return self.selector.get_by_id(user_id)

    def create_user(self, data: dict[str, Any]):
        return self.repository.create(data)

    def update_user(self, user_id: str, data: dict[str, Any]):
        user = self.selector.get_by_id(user_id)
        data = data.copy()
        #aqui se hace el cambio de contraseña
        if "password" in data:
            password = data.pop("password")
            user.set_password(password)
        return self.repository.update(user, data)

    def delete_user(self, user_id: str) -> None:
        user = self.selector.get_by_id(user_id)
        self.repository.delete(user)
