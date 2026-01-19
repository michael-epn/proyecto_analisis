import random
from dotenv import load_dotenv
from pymongo import MongoClient
import sys

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()


uri = "mongodb+srv://maykolaicogg3_db_user:KrwVu5AGD1wtGizL@datos.wrq4154.mongodb.net/?appName=Datos"

def insertar_datos_sucios_mongo():
    catalogo_insumos = {
        "Quintal Harina Trigo": {"base": 45.00, "cat": "Materia Prima", "provs": ["Moderna", "Santa Lucia"]},
        "Litro Leche Entera": {"base": 0.90, "cat": "Lácteos", "provs": ["Vita", "Rey Leche"]},
        "Cubeta Huevos (30u)": {"base": 3.50, "cat": "Materia Prima", "provs": ["Indaves", "Avícola"]},
        "Margarina Industrial": {"base": 2.50, "cat": "Grasas", "provs": ["Danec", "La Fabril"]},
        "Esencia Vainilla": {"base": 12.00, "cat": "Esencias", "provs": ["DelyClar"]},
        "Chocolate Cobertura": {"base": 8.50, "cat": "Repostería", "provs": ["Pacari", "Cordillera"]}
    }
    
    client = MongoClient(uri)
    db = client["Panaderia"]
    coleccion = db["Insumos"]
    
    lista_para_mongo = []
    items = list(catalogo_insumos.keys())
    print("Generando insumos sucios para MongoDB...")

    for i in range(500, 600):
        nombre_item = random.choice(items)
        info = catalogo_insumos[nombre_item]
        
        precio_real = round(info["base"] * random.uniform(0.95, 1.05), 2)
        
        documento = {
            "id_insumo": i,
            "nombre": nombre_item,
            "precio_compra": str(precio_real),
            "categoria": info["cat"],
            "stock": str(random.randint(0, 300)),
            "proveedor": random.choice(info["provs"]),
        }
        
        if random.random() < 0.45:
            ruido = random.choice(["error", "N/A", "", "null", "NaN"])
            campo_ruido = random.choice(["precio_compra", "stock", "proveedor"])
            documento[campo_ruido] = ruido
            
        lista_para_mongo.append(documento)
        
    try:
        resultado = coleccion.insert_many(lista_para_mongo)
        print(f"Conectado. Se insertaron {len(resultado.inserted_ids)} insumos con éxito.")
        
    except Exception as e:
        print(f"Error en la inserción: {e}")

insertar_datos_sucios_mongo()