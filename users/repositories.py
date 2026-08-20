from __future__ import annotations
from typing import Any
from users.models import User

class UserRepository:
    def create(self, data: dict[str, Any]) -> User:
        return User.objects.create_user(**data)

    def update(self, user: User, data: dict[str, Any]) -> User:
        for field, value in data.items():
            setattr(user, field, value)
        user.save()
        return user

    def delete(self, user: User) -> None:
        user.delete()