"""
Pruebas de HU-01 (registrar productos) y del filtro por categoría.

CA-01.1  Valida que el código no exista y que el precio sea mayor a cero.
CA-01.2  El producto se guarda y aparece en la lista general.
"""

from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from apps.usuarios.models import Rol, Usuario

from .models import Categoria, Marca, Producto, UnidadMedida

URL_PRODUCTOS = '/api/catalogo/productos/'


class ProductoApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        rol_admin = Rol.objects.create(nombre=Rol.ADMINISTRADOR)
        rol_cajero = Rol.objects.create(nombre=Rol.CAJERO)
        cls.admin = Usuario.objects.create_user('admin', 'Administrador', 'clave-prueba-123', rol=rol_admin)
        cls.cajero = Usuario.objects.create_user('cajero', 'Cajero', 'clave-prueba-123', rol=rol_cajero)

        cls.manuales = Categoria.objects.create(nombre='Herramientas manuales')
        cls.electricas = Categoria.objects.create(nombre='Herramientas eléctricas')
        cls.truper = Marca.objects.create(nombre='Truper')
        cls.unidad = UnidadMedida.objects.create(nombre='Unidad', abreviatura='UND')

    def setUp(self):
        self.client.force_authenticate(self.admin)

    def datos_producto(self, **cambios):
        datos = {
            'codigo': 'HER-0012',
            'nombre': 'Martillo de uña 16 oz',
            'precio_compra': '17.50',
            'precio_venta': '25.90',
            'stock': '40',
            'stock_minimo': '5',
            'categoria': self.manuales.pk,
            'marca': self.truper.pk,
            'unidad': self.unidad.pk,
        }
        datos.update(cambios)
        return datos

    # CA-01.2: el producto se guarda y aparece en la lista general
    def test_registrar_producto_y_aparece_en_la_lista(self):
        respuesta = self.client.post(URL_PRODUCTOS, self.datos_producto(), format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.get(codigo='HER-0012').precio_venta, Decimal('25.90'))

        lista = self.client.get(URL_PRODUCTOS).json()
        self.assertIn('HER-0012', [p['codigo'] for p in lista])

    # CA-01.1: el código no debe existir
    def test_no_permite_codigo_duplicado(self):
        self.client.post(URL_PRODUCTOS, self.datos_producto(), format='json')
        respuesta = self.client.post(URL_PRODUCTOS, self.datos_producto(nombre='Otro'), format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('codigo', respuesta.json())
        self.assertEqual(Producto.objects.count(), 1)

    def test_codigo_duplicado_sin_importar_mayusculas(self):
        self.client.post(URL_PRODUCTOS, self.datos_producto(), format='json')
        respuesta = self.client.post(URL_PRODUCTOS, self.datos_producto(codigo='her-0012'), format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)

    # CA-01.1: el precio debe ser mayor a cero
    def test_no_permite_precio_cero(self):
        respuesta = self.client.post(URL_PRODUCTOS, self.datos_producto(precio_venta='0'), format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('precio_venta', respuesta.json())

    def test_no_permite_precio_negativo(self):
        respuesta = self.client.post(URL_PRODUCTOS, self.datos_producto(precio_venta='-5'), format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_permite_stock_negativo(self):
        respuesta = self.client.post(URL_PRODUCTOS, self.datos_producto(stock='-1'), format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('stock', respuesta.json())

    def test_acepta_stock_con_decimales(self):
        respuesta = self.client.post(
            URL_PRODUCTOS, self.datos_producto(codigo='ELC-0077', stock='2.5'), format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)

    def test_campos_obligatorios(self):
        respuesta = self.client.post(URL_PRODUCTOS, {}, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        for campo in ('codigo', 'nombre', 'precio_venta', 'categoria', 'unidad'):
            self.assertIn(campo, respuesta.json())

    # Filtro por categoría
    def test_filtrar_por_categoria(self):
        self.client.post(URL_PRODUCTOS, self.datos_producto(), format='json')
        self.client.post(URL_PRODUCTOS, self.datos_producto(
            codigo='ELE-0105', nombre='Taladro percutor', categoria=self.electricas.pk), format='json')

        lista = self.client.get(URL_PRODUCTOS, {'categoria': self.electricas.pk}).json()
        self.assertEqual([p['codigo'] for p in lista], ['ELE-0105'])

    def test_buscar_por_codigo_o_nombre(self):
        self.client.post(URL_PRODUCTOS, self.datos_producto(), format='json')
        self.assertEqual(len(self.client.get(URL_PRODUCTOS, {'buscar': 'marti'}).json()), 1)
        self.assertEqual(len(self.client.get(URL_PRODUCTOS, {'buscar': 'HER-00'}).json()), 1)
        self.assertEqual(len(self.client.get(URL_PRODUCTOS, {'buscar': 'taladro'}).json()), 0)

    # Borrado lógico: no se elimina, se desactiva
    def test_eliminar_desactiva_el_producto(self):
        creado = self.client.post(URL_PRODUCTOS, self.datos_producto(), format='json').json()
        respuesta = self.client.delete(f"{URL_PRODUCTOS}{creado['id_producto']}/")
        self.assertEqual(respuesta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Producto.objects.get(pk=creado['id_producto']).estado)
        self.assertEqual(self.client.get(URL_PRODUCTOS).json(), [])

    # Permisos por rol
    def test_cajero_puede_consultar_pero_no_registrar(self):
        self.client.force_authenticate(self.cajero)
        self.assertEqual(self.client.get(URL_PRODUCTOS).status_code, status.HTTP_200_OK)
        respuesta = self.client.post(URL_PRODUCTOS, self.datos_producto(), format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_403_FORBIDDEN)

    def test_sin_sesion_no_hay_acceso(self):
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get(URL_PRODUCTOS).status_code, status.HTTP_401_UNAUTHORIZED)


class LoginApiTests(APITestCase):

    def test_login_devuelve_token_con_rol(self):
        rol = Rol.objects.create(nombre=Rol.ADMINISTRADOR)
        Usuario.objects.create_user('ana', 'Ana', 'clave-prueba-123', rol=rol)
        respuesta = self.client.post(
            '/api/auth/login/', {'usuario': 'ana', 'password': 'clave-prueba-123'}, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        datos = respuesta.json()
        self.assertIn('access', datos)
        self.assertEqual(datos['usuario']['rol'], Rol.ADMINISTRADOR)

    def test_login_con_clave_incorrecta(self):
        rol = Rol.objects.create(nombre=Rol.CAJERO)
        Usuario.objects.create_user('ana', 'Ana', 'clave-prueba-123', rol=rol)
        respuesta = self.client.post(
            '/api/auth/login/', {'usuario': 'ana', 'password': 'otra'}, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_401_UNAUTHORIZED)
