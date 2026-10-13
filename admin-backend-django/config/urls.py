from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.usuarios.urls')),
    path('api/catalogo/', include('apps.catalogo.urls')),
    # Botón "Iniciar sesión" de la API navegable (para probar en el navegador)
    path('api-auth/', include('rest_framework.urls')),
]
