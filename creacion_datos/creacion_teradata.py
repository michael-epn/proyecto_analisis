import teradatasql
import random
import sys

sys.stdout.reconfigure(encoding='utf-8')

host = '192.168.100.25'
user = 'dbc'
password = 'dbc'

def generar_datos_sucios_teradata(id_range):
    catalogo_insumos = {
        "Quintal Harina Trigo": {"base": 45.00, "cat": "Materia Prima", "provs": ["Moderna"]},
        "Litro Leche Entera": {"base": 0.90, "cat": "Lácteos", "provs": ["Vita", "Rey Leche"]},
        "Cubeta Huevos (30u)": {"base": 3.50, "cat": "Materia Prima", "provs": ["Indaves"]},
        "Margarina Industrial": {"base": 2.50, "cat": "Grasas", "provs": ["Danec", "La Fabril"]},
        "Chocolate Cobertura": {"base": 8.50, "cat": "Repostería", "provs": ["Pacari"]}
    }
    
    items = list(catalogo_insumos.keys())
    data = []
    
    for i in id_range:
        nombre = random.choice(items)
        info = catalogo_insumos[nombre]
        
        pc = round(info["base"] * random.uniform(0.98, 1.02), 2)
        
        p_compra = str(pc)
        cat = info["cat"]
        stock = str(random.randint(10, 500))
        prov = random.choice(info["provs"])
        
        if random.random() < 0.45:
            ruido = random.choice(["error", "N/A", "", "NULL", "NaN"])
            campo_ruido = random.choice(["p_compra", "stock", "prov", "cat"])
            
            if campo_ruido == "p_compra": p_compra = ruido
            elif campo_ruido == "stock": stock = ruido
            elif campo_ruido == "prov": prov = ruido
            elif campo_ruido == "cat": cat = ruido
            
        data.append((i, nombre, p_compra, cat, stock, prov))
        
    return data

datos_para_insertar = generar_datos_sucios_teradata(range(400, 500))

try:
    with teradatasql.connect(host=host, user=user, password=password) as connect:
        with connect.cursor() as cursor:
            print(f"Conectado a {host}. Insertando insumos sucios...")
            cursor.executemany(
                "INSERT INTO Panaderia.Insumos VALUES (?, ?, ?, ?, ?, ?)", 
                datos_para_insertar
            )
            print("Inserción completada exitosamente.")
except Exception as e:
    print(f"Error al insertar en Teradata: {e}")