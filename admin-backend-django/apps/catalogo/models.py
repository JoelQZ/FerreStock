from django.db import models
from django.db.models import Q


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'categoria'
        ordering = ['nombre']
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60, unique=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'marca'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class UnidadMedida(models.Model):
    id_unidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, unique=True)
    abreviatura = models.CharField(max_length=10)

    class Meta:
        db_table = 'unidad_medida'
        ordering = ['nombre']
        verbose_name = 'unidad de medida'
        verbose_name_plural = 'unidades de medida'

    def __str__(self):
        return f'{self.nombre} ({self.abreviatura})'


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=120, db_index=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    # DECIMAL porque la ferretería vende por metro y por kilo (ej.: 2.5 m de cable)
    stock = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, db_column='id_categoria',
                                  related_name='productos')
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, db_column='id_marca',
                              related_name='productos', blank=True, null=True)
    unidad = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, db_column='id_unidad',
                               related_name='productos', verbose_name='unidad de medida')
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'producto'
        ordering = ['nombre']
        constraints = [
            models.CheckConstraint(condition=Q(precio_venta__gt=0),
                                   name='producto_precio_venta_mayor_cero'),
            models.CheckConstraint(condition=Q(precio_compra__gte=0),
                                   name='producto_precio_compra_no_negativo'),
            models.CheckConstraint(condition=Q(stock__gte=0),
                                   name='producto_stock_no_negativo'),
            models.CheckConstraint(condition=Q(stock_minimo__gte=0),
                                   name='producto_stock_minimo_no_negativo'),
        ]

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
