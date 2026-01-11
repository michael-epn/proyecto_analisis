import random
from dotenv import load_dotenv
from pymongo import MongoClient
import sys
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
uri = "mongodb+srv://maykolaicogg3_db_user:dtx9HPwoOknYKFfW@datos.wrq4154.mongodb.net/?appName=Datos"

productos = ["Pan de Masa Madre", "Pastel de Chocolate", "Pan de Leche", "Galletas", "Cacho", "Gusano", "Donas"]
categorias = ["Panadería", "Pastelería", "Insumos", "Cafetería"]
proveedores = ["Moderna", "Vita", "DelyClar"]

def insertar_datos_sucios_mongo():
    client = MongoClient(uri)
    db = client["Panaderia"]
    coleccion = db["Productos"]
    
    lista_para_mongo = []
    print("Generando datos sucios para MongoDB...")

    for i in range(500, 600):
        pc = round(random.uniform(0.50, 15.00), 2)
        
        documento = {
            "id_producto": i,
            "nombre": random.choice(productos),
            "precio_compra": str(pc),
            "categoria": random.choice(categorias),
            "stock": str(random.randint(0, 300)),
            "proveedor": random.choice(proveedores),
            "precio_venta_publico": str(round(pc * 1.5, 2))
        }
        
        if random.random() < 0.15:
            ruido = random.choice(["error", "N/A", "", "texto", "NaN"])
            campo_ruido = random.choice(["precio_compra", "stock", "proveedor", "precio_venta_publico", "nombre", "categoria"])
            documento[campo_ruido] = ruido
            
        lista_para_mongo.append(documento)
        
    try:
        resultado = coleccion.insert_many(lista_para_mongo)
        print(f"Conectado. Se insertaron {len(resultado.inserted_ids)} documentos con éxito.")
        
    except Exception as e:
        print(f"Error en la inserción: {e}")

insertar_datos_sucios_mongo()