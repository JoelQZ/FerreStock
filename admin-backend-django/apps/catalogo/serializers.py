from rest_framework import serializers

from .models import Categoria, Marca, Producto, UnidadMedida


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id_categoria', 'nombre', 'descripcion', 'estado')


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ('id_marca', 'nombre', 'estado')


class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = ('id_unidad', 'nombre', 'abreviatura')


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True, default=None)
    unidad_abreviatura = serializers.CharField(source='unidad.abreviatura', read_only=True)
    stock_bajo = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = (
            'id_producto', 'codigo', 'nombre', 'descripcion',
            'precio_compra', 'precio_venta', 'stock', 'stock_minimo',
            'categoria', 'categoria_nombre', 'marca', 'marca_nombre',
            'unidad', 'unidad_abreviatura', 'estado', 'stock_bajo',
        )
        # La unicidad del código se valida en validate_codigo, con mensaje propio.
        extra_kwargs = {'codigo': {'validators': []}}

    def get_stock_bajo(self, obj):
        return obj.stock <= obj.stock_minimo

    # CA-01: el código no debe existir.
    def validate_codigo(self, valor):
        valor = valor.strip()
        if not valor:
            raise serializers.ValidationError('El código es obligatorio.')
        repetidos = Producto.objects.filter(codigo__iexact=valor)
        if self.instance:
            repetidos = repetidos.exclude(pk=self.instance.pk)
        if repetidos.exists():
            raise serializers.ValidationError('Ya existe un producto con este código.')
        return valor

    # CA-01: el precio debe ser mayor a cero.
    def validate_precio_venta(self, valor):
        if valor <= 0:
            raise serializers.ValidationError('El precio de venta debe ser mayor a cero.')
        return valor

    def validate_precio_compra(self, valor):
        if valor < 0:
            raise serializers.ValidationError('El precio de compra no puede ser negativo.')
        return valor

    def validate_stock(self, valor):
        if valor < 0:
            raise serializers.ValidationError('El stock no puede ser negativo.')
        return valor

    def validate_stock_minimo(self, valor):
        if valor < 0:
            raise serializers.ValidationError('El stock mínimo no puede ser negativo.')
        return valor

    def validate_categoria(self, categoria):
        if not categoria.estado:
            raise serializers.ValidationError('La categoría está desactivada.')
        return categoria
