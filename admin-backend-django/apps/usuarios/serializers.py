from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Usuario


class LoginSerializer(TokenObtainPairSerializer):
    """Token JWT que además lleva el nombre y el rol del usuario.
    React y Spring Boot leen el rol desde el token."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['nombre'] = user.nombre
        token['rol'] = user.rol.nombre
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['usuario'] = UsuarioSerializer(self.user).data
        return data


class UsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(source='rol.nombre', read_only=True)

    class Meta:
        model = Usuario
        fields = ('id_usuario', 'usuario', 'nombre', 'rol')
