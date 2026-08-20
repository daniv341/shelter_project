from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from users.models import User


class UserSelector:
    def get_by_id(self, user_id: str) -> User:
        return get_object_or_404(User, pk=user_id)

    def get_all(self) -> QuerySet[User]:
        return User.objects.all()
