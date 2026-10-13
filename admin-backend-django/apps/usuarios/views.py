from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LoginSerializer, UsuarioSerializer


class LoginView(TokenObtainPairView):
    """POST /api/auth/login/ con {"usuario": "...", "password": "..."}"""

    serializer_class = LoginSerializer


@api_view(['GET'])
def usuario_actual(request):
    """GET /api/auth/yo/: datos del usuario que inició sesión."""
    return Response(UsuarioSerializer(request.user).data)
