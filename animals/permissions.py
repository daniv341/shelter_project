"""
permissions.py

Permisos personalizados del módulo animals.

Por ahora el endpoint es de acceso libre (AllowAny, configurado en
settings.REST_FRAMEWORK) porque la autenticación JWT aún no está
implementada. Esta clase queda lista para cuando se active Simple JWT:
por ejemplo, se podría restringir escritura a usuarios de staff y
dejar lectura abierta.
"""
from __future__ import annotations

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsStaffOrReadOnly(BasePermission):
    """Lectura libre; escritura solo para usuarios staff/autenticados.

    No está activo por defecto todavía (ver DEFAULT_PERMISSION_CLASSES
    en settings.py); se deja implementado para conectarlo cuando se
    incorpore la autenticación JWT.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
