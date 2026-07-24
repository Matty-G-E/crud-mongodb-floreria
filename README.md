# CRUD de Florería con MongoDB y Python

Proyecto de evaluación integradora para Bases de Datos No Estructuradas.

## Descripción

Sistema CRUD de consola desarrollado en Python 3 con PyMongo y MongoDB local.

La colección `pedidos` incluye:

- Subdocumento: `contacto`
- Array de subdocumentos: `productos`
- Campo de fecha: `fecha_pedido`

El sistema precarga automáticamente 8 documentos si la colección está vacía.

## Requisitos

- Python 3
- MongoDB Community Server
- Git
- PyMongo

## Instalación

1. Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
cd NOMBRE_DEL_REPOSITORIO
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Verificar que MongoDB esté iniciado en:

```text
mongodb://localhost:27017
```

4. Ejecutar:

```bash
python main.py
```

## Funcionalidades

1. Crear documento completo.
2. Listar todos los documentos.
3. Buscar por comparación usando `$gte` y `$lte`.
4. Buscar por texto usando `$regex`.
5. Buscar por rango de fechas.
6. Buscar dentro de un array de subdocumentos.
7. Actualizar un campo raíz usando `$set`.
8. Actualizar un array usando `$push` y el total usando `$inc`.
9. Eliminar un documento con condición y confirmación.

## Base de datos

- Base de datos: `floreria_db`
- Colección: `pedidos`
