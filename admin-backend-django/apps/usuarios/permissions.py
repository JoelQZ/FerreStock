from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Rol


class EsAdministradorOLectura(BasePermission):
    """Cualquier usuario con sesión puede consultar; solo el administrador
    y el dueño pueden crear, editar o desactivar."""

    message = 'Solo el administrador o el dueño pueden modificar el catálogo.'

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_superuser or user.rol.nombre in (Rol.ADMINISTRADOR, Rol.DUENO)
