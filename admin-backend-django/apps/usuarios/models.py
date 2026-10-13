from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Rol(models.Model):
    ADMINISTRADOR = 'ADMINISTRADOR'
    CAJERO = 'CAJERO'
    DUENO = 'DUENO'

    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'rol'
        verbose_name = 'rol'
        verbose_name_plural = 'roles'

    def __str__(self):
        return self.nombre


class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, nombre, password=None, rol=None, **extra):
        if not usuario:
            raise ValueError('El usuario es obligatorio')
        if rol is None:
            rol = Rol.objects.get(nombre=Rol.CAJERO)
        user = self.model(usuario=usuario, nombre=nombre, rol=rol, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, nombre, password=None, **extra):
        rol, _ = Rol.objects.get_or_create(nombre=Rol.DUENO)
        extra['is_superuser'] = True
        return self.create_user(usuario, nombre, password, rol=rol, **extra)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, db_column='id_rol', related_name='usuarios')
    estado = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['nombre']

    class Meta:
        db_table = 'usuario'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return f'{self.nombre} ({self.usuario})'

    # Borrado lógico: un usuario con estado = 0 no puede iniciar sesión.
    @property
    def is_active(self):
        return self.estado

    # Entran al panel /admin el administrador y el dueño.
    @property
    def is_staff(self):
        return self.is_superuser or self.rol.nombre in (Rol.ADMINISTRADOR, Rol.DUENO)
