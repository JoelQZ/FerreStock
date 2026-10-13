from django.db.models import Q
from rest_framework import viewsets

from apps.usuarios.permissions import EsAdministradorOLectura

from .models import Categoria, Marca, Producto, UnidadMedida
from .serializers import (
    CategoriaSerializer, MarcaSerializer, ProductoSerializer, UnidadMedidaSerializer,
)


def solo_activos(request):
    """Por defecto se listan solo los registros activos; ?todos=1 incluye los desactivados."""
    return request.query_params.get('todos') != '1'


class BorradoLogicoMixin:
    """Regla de negocio: catálogos y productos no se eliminan, se desactivan (estado = 0)."""

    def perform_destroy(self, instance):
        instance.estado = False
        instance.save(update_fields=['estado'])


class CategoriaViewSet(BorradoLogicoMixin, viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [EsAdministradorOLectura]

    def get_queryset(self):
        qs = Categoria.objects.all()
        return qs.filter(estado=True) if solo_activos(self.request) else qs


class MarcaViewSet(BorradoLogicoMixin, viewsets.ModelViewSet):
    serializer_class = MarcaSerializer
    permission_classes = [EsAdministradorOLectura]

    def get_queryset(self):
        qs = Marca.objects.all()
        return qs.filter(estado=True) if solo_activos(self.request) else qs


class UnidadMedidaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer
    permission_classes = [EsAdministradorOLectura]


class ProductoViewSet(BorradoLogicoMixin, viewsets.ModelViewSet):
    """
    /api/catalogo/productos/
      ?categoria=<id>   filtra por categoría
      ?buscar=<texto>   busca por código o nombre
      ?todos=1          incluye productos desactivados
    """

    serializer_class = ProductoSerializer
    permission_classes = [EsAdministradorOLectura]

    def get_queryset(self):
        qs = Producto.objects.select_related('categoria', 'marca', 'unidad')
        params = self.request.query_params
        if solo_activos(self.request):
            qs = qs.filter(estado=True)
        if params.get('categoria'):
            qs = qs.filter(categoria_id=params['categoria'])
        if params.get('buscar'):
            texto = params['buscar'].strip()
            qs = qs.filter(Q(codigo__icontains=texto) | Q(nombre__icontains=texto))
        return qs
