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
    # comprobar si el usuario tiene permisos para realizar la acción
    def has_permission(self, request: Request, view: APIView) -> bool:
        # permitir el acceso si el método es seguro (GET, HEAD, OPTIONS) o si el usuario es staff
        if request.method in SAFE_METHODS:
            return True
        # permitir el acceso si el usuario es staff
        return bool(request.user and request.user.is_staff)