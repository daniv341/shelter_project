from __future__ import annotations

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

class IsActiveUser(BasePermission):
    message = "El usuario no está activo."
    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user

        return bool(user and user.is_authenticated and user.is_active)

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if not user.is_active:
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_staff
