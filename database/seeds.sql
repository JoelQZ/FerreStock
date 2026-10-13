-- FerreStock · Datos iniciales
-- Ejecutar en MySQL Workbench DESPUÉS de `python manage.py migrate`
-- (las tablas las crea Django).

USE ferrestock;

INSERT INTO rol (nombre, descripcion) VALUES
 ('ADMINISTRADOR', 'Gestiona productos, inventario y alertas'),
 ('CAJERO',        'Realiza ventas, cobros y cierre de caja'),
 ('DUENO',         'Consulta reportes y tiene acceso total');

INSERT INTO unidad_medida (nombre, abreviatura) VALUES
 ('Unidad',    'UND'),
 ('Metro',     'M'),
 ('Kilogramo', 'KG'),
 ('Caja',      'CJA'),
 ('Galón',     'GAL');
