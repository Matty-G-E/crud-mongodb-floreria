from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

URI = "mongodb://localhost:27017"
DB_NAME = "floreria_db"
COLLECTION_NAME = "pedidos"

def conectar():
    try:
        cliente = MongoClient(URI, serverSelectionTimeoutMS=3000)
        cliente.admin.command("ping")
        print("✅ Conexión exitosa a MongoDB")
        return cliente, cliente[DB_NAME][COLLECTION_NAME]
    except ServerSelectionTimeoutError:
        print("❌ No se pudo conectar a MongoDB.")
        print("Verifica que el servicio MongoDB esté iniciado en localhost:27017.")
        raise SystemExit(1)

def fecha_desde_texto(texto):
    return datetime.strptime(texto, "%Y-%m-%d")

def mostrar_documento(doc):
    if not doc:
        print("No se encontró el documento.")
        return
    print("-" * 60)
    print(f"ID: {doc.get('_id')}")
    print(f"Cliente: {doc.get('cliente')}")
    print(f"Total: ${doc.get('total')}")
    print(f"Estado: {doc.get('estado')}")
    fecha = doc.get("fecha_pedido")
    print(f"Fecha: {fecha.strftime('%Y-%m-%d') if isinstance(fecha, datetime) else fecha}")
    contacto = doc.get("contacto", {})
    print(f"Contacto: {contacto.get('telefono')} | {contacto.get('correo')}")
    print("Productos:")
    for producto in doc.get("productos", []):
        print(f"  - {producto.get('nombre')} | Cantidad: {producto.get('cantidad')} | Precio: ${producto.get('precio')}")
    print("-" * 60)

def cargar_datos_iniciales(coleccion):
    if coleccion.count_documents({}) > 0:
        return
    datos = [
        {
            "cliente": "Ana Torres",
            "total": 25000,
            "estado": "Pendiente",
            "contacto": {"telefono": "912345671", "correo": "ana@email.com"},
            "productos": [{"nombre": "Ramo de rosas", "cantidad": 1, "precio": 25000}],
            "fecha_pedido": datetime(2026, 7, 10)
        },
        {
            "cliente": "Bruno Díaz",
            "total": 18000,
            "estado": "Entregado",
            "contacto": {"telefono": "912345672", "correo": "bruno@email.com"},
            "productos": [{"nombre": "Tulipanes", "cantidad": 2, "precio": 9000}],
            "fecha_pedido": datetime(2026, 7, 12)
        },
        {
            "cliente": "Carla Soto",
            "total": 32000,
            "estado": "Preparando",
            "contacto": {"telefono": "912345673", "correo": "carla@email.com"},
            "productos": [
                {"nombre": "Lirios", "cantidad": 1, "precio": 20000},
                {"nombre": "Chocolates", "cantidad": 1, "precio": 12000}
            ],
            "fecha_pedido": datetime(2026, 7, 14)
        },
        {
            "cliente": "Diego Rojas",
            "total": 15000,
            "estado": "Entregado",
            "contacto": {"telefono": "912345674", "correo": "diego@email.com"},
            "productos": [{"nombre": "Girasoles", "cantidad": 3, "precio": 5000}],
            "fecha_pedido": datetime(2026, 7, 16)
        },
        {
            "cliente": "Elena Muñoz",
            "total": 42000,
            "estado": "Pendiente",
            "contacto": {"telefono": "912345675", "correo": "elena@email.com"},
            "productos": [{"nombre": "Arreglo premium", "cantidad": 1, "precio": 42000}],
            "fecha_pedido": datetime(2026, 7, 18)
        },
        {
            "cliente": "Felipe Castro",
            "total": 21000,
            "estado": "Preparando",
            "contacto": {"telefono": "912345676", "correo": "felipe@email.com"},
            "productos": [{"nombre": "Rosas blancas", "cantidad": 1, "precio": 21000}],
            "fecha_pedido": datetime(2026, 7, 20)
        },
        {
            "cliente": "Gabriela León",
            "total": 27000,
            "estado": "Entregado",
            "contacto": {"telefono": "912345677", "correo": "gabriela@email.com"},
            "productos": [{"nombre": "Orquídea", "cantidad": 1, "precio": 27000}],
            "fecha_pedido": datetime(2026, 7, 22)
        },
        {
            "cliente": "Héctor Silva",
            "total": 35000,
            "estado": "Pendiente",
            "contacto": {"telefono": "912345678", "correo": "hector@email.com"},
            "productos": [
                {"nombre": "Ramo mixto", "cantidad": 1, "precio": 28000},
                {"nombre": "Tarjeta", "cantidad": 1, "precio": 7000}
            ],
            "fecha_pedido": datetime(2026, 7, 24)
        }
    ]
    resultado = coleccion.insert_many(datos)
    print(f"✅ Se precargaron {len(resultado.inserted_ids)} documentos.")

def crear_documento(coleccion):
    try:
        cliente = input("Nombre del cliente: ").strip()
        total = int(input("Total del pedido: "))
        estado = input("Estado: ").strip()
        telefono = input("Teléfono: ").strip()
        correo = input("Correo: ").strip()
        fecha = fecha_desde_texto(input("Fecha del pedido (YYYY-MM-DD): ").strip())

        productos = []
        cantidad_productos = int(input("¿Cuántos productos desea agregar?: "))
        for i in range(cantidad_productos):
            print(f"\nProducto {i + 1}")
            nombre = input("Nombre: ").strip()
            cantidad = int(input("Cantidad: "))
            precio = int(input("Precio unitario: "))
            productos.append({"nombre": nombre, "cantidad": cantidad, "precio": precio})

        documento = {
            "cliente": cliente,
            "total": total,
            "estado": estado,
            "contacto": {"telefono": telefono, "correo": correo},
            "productos": productos,
            "fecha_pedido": fecha
        }
        resultado = coleccion.insert_one(documento)
        print(f"✅ Documento insertado con ID: {resultado.inserted_id}")
    except ValueError:
        print("❌ Datos inválidos. Verifica números y fecha.")

def listar_documentos(coleccion):
    documentos = list(coleccion.find({}, {
        "cliente": 1, "total": 1, "estado": 1, "contacto": 1,
        "productos": 1, "fecha_pedido": 1
    }))
    print(f"\nTotal de documentos: {len(documentos)}")
    for doc in documentos:
        mostrar_documento(doc)

def buscar_comparacion(coleccion):
    try:
        minimo = int(input("Total mínimo: "))
        maximo = int(input("Total máximo: "))
        resultados = coleccion.find({
            "total": {"$gte": minimo, "$lte": maximo}
        })
        encontrados = 0
        for doc in resultados:
            mostrar_documento(doc)
            encontrados += 1
        print(f"✅ Resultados encontrados: {encontrados}")
    except ValueError:
        print("❌ Debes ingresar números válidos.")

def buscar_regex(coleccion):
    texto = input("Texto a buscar en el nombre del cliente: ").strip()
    resultados = coleccion.find({
        "cliente": {"$regex": texto, "$options": "i"}
    })
    encontrados = 0
    for doc in resultados:
        mostrar_documento(doc)
        encontrados += 1
    print(f"✅ Resultados encontrados: {encontrados}")

def buscar_fechas(coleccion):
    try:
        inicio = fecha_desde_texto(input("Fecha inicial (YYYY-MM-DD): ").strip())
        fin = fecha_desde_texto(input("Fecha final (YYYY-MM-DD): ").strip())
        resultados = coleccion.find({
            "fecha_pedido": {"$gte": inicio, "$lte": fin}
        })
        encontrados = 0
        for doc in resultados:
            mostrar_documento(doc)
            encontrados += 1
        print(f"✅ Resultados encontrados: {encontrados}")
    except ValueError:
        print("❌ Formato de fecha inválido.")

def buscar_anidado(coleccion):
    texto = input("Producto a buscar: ").strip()
    resultados = coleccion.find({
        "productos.nombre": {"$regex": texto, "$options": "i"}
    })
    encontrados = 0
    for doc in resultados:
        mostrar_documento(doc)
        encontrados += 1
    print(f"✅ Resultados encontrados: {encontrados}")

def actualizar_raiz(coleccion):
    cliente = input("Cliente cuyo estado desea actualizar: ").strip()
    antes = coleccion.find_one({"cliente": {"$regex": f"^{cliente}$", "$options": "i"}})
    if not antes:
        print("❌ Cliente no encontrado.")
        return
    print("\nDocumento antes de actualizar:")
    mostrar_documento(antes)
    nuevo_estado = input("Nuevo estado: ").strip()
    resultado = coleccion.update_one(
        {"_id": antes["_id"]},
        {"$set": {"estado": nuevo_estado}}
    )
    despues = coleccion.find_one({"_id": antes["_id"]})
    print(f"✅ Documentos modificados: {resultado.modified_count}")
    print("\nDocumento después de actualizar:")
    mostrar_documento(despues)

def actualizar_anidado(coleccion):
    cliente = input("Cliente al que agregará un producto: ").strip()
    antes = coleccion.find_one({"cliente": {"$regex": f"^{cliente}$", "$options": "i"}})
    if not antes:
        print("❌ Cliente no encontrado.")
        return
    print("\nDocumento antes de actualizar:")
    mostrar_documento(antes)
    try:
        nombre = input("Nombre del nuevo producto: ").strip()
        cantidad = int(input("Cantidad: "))
        precio = int(input("Precio: "))
        resultado = coleccion.update_one(
            {"_id": antes["_id"]},
            {
                "$push": {
                    "productos": {
                        "nombre": nombre,
                        "cantidad": cantidad,
                        "precio": precio
                    }
                },
                "$inc": {"total": cantidad * precio}
            }
        )
        despues = coleccion.find_one({"_id": antes["_id"]})
        print(f"✅ Documentos modificados: {resultado.modified_count}")
        print("\nDocumento después de actualizar:")
        mostrar_documento(despues)
    except ValueError:
        print("❌ Cantidad o precio inválido.")

def eliminar_documento(coleccion):
    cliente = input("Cliente cuyo pedido desea eliminar: ").strip()
    documento = coleccion.find_one({"cliente": {"$regex": f"^{cliente}$", "$options": "i"}})
    if not documento:
        print("❌ Cliente no encontrado.")
        return
    print("\nDocumento que se eliminará:")
    mostrar_documento(documento)
    confirmar = input("¿Confirmar eliminación? (s/n): ").strip().lower()
    if confirmar == "s":
        resultado = coleccion.delete_one({"_id": documento["_id"]})
        print(f"✅ Documentos eliminados: {resultado.deleted_count}")
    else:
        print("Operación cancelada.")

def mostrar_menu():
    print("""
================ CRUD FLORERÍA ================
1. Crear documento
2. Listar todos los documentos
3. Buscar por comparación de total
4. Buscar cliente con expresión regular
5. Buscar por rango de fechas
6. Buscar dentro del array de productos
7. Actualizar campo raíz (estado)
8. Actualizar array de subdocumentos (agregar producto)
9. Eliminar documento con condición
0. Salir
================================================
""")

def main():
    cliente, coleccion = conectar()
    cargar_datos_iniciales(coleccion)

    opciones = {
        "1": crear_documento,
        "2": listar_documentos,
        "3": buscar_comparacion,
        "4": buscar_regex,
        "5": buscar_fechas,
        "6": buscar_anidado,
        "7": actualizar_raiz,
        "8": actualizar_anidado,
        "9": eliminar_documento,
    }

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            print("Programa finalizado.")
            cliente.close()
            break
        funcion = opciones.get(opcion)
        if funcion:
            funcion(coleccion)
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    main()
