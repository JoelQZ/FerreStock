from django.contrib import admin

from .models import Categoria, Marca, Producto, UnidadMedida


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre',)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre',)


@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'abreviatura')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'marca', 'unidad',
                    'precio_venta', 'stock', 'stock_minimo', 'estado')
    list_filter = ('categoria', 'marca', 'estado')   # filtro por categoría (HU-04)
    search_fields = ('codigo', 'nombre')             # búsqueda por código o nombre
    list_per_page = 25
