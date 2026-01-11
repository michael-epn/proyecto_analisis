import teradatasql
import random
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Configuración de conexión
host = '192.168.100.25'
user = 'dbc'
password = 'dbc'

def generar_datos_sucios_teradata(id_range):
    productos = ["Pan de Masa Madre", "Pastel de Chocolate", "Pan de Leche", "Galletas", "Cacho", "Gusano", "Donas"]
    categorias = ["Panadería", "Pastelería", "Insumos", "Cafetería"]
    proveedores = ["Moderna", "Vita", "DelyClar", "Pacari"]
    
    data = []
    for i in id_range:
        pc = round(random.uniform(0.5, 20.0), 2)
        nombre = random.choice(productos)
        p_compra = str(pc)
        cat = random.choice(categorias)
        stock = str(random.randint(0, 300))
        prov = random.choice(proveedores)
        p_venta = str(round(pc * 1.5, 2))
        
        if random.random() < 0.15:
            ruido = random.choice(["error", "N/A", "", "texto", "NaN"])
            campo_ruido = random.choice(["p_compra", "stock", "prov", "p_venta", "nombre", "cat"])
            
            if campo_ruido == "p_compra": p_compra = ruido
            elif campo_ruido == "stock": stock = ruido
            elif campo_ruido == "prov": prov = ruido
            elif campo_ruido == "p_venta": p_venta = ruido
            elif campo_ruido == "nombre": nombre = ruido
            elif campo_ruido == "cat": cat = ruido
            
        data.append((i, nombre, p_compra, cat, stock, prov, p_venta))
    return data

datos_para_insertar = generar_datos_sucios_teradata(range(400, 500))

try:
    with teradatasql.connect(host=host, user=user, password=password) as connect:
        with connect.cursor() as cursor:
            print(f"Conectado a {host}. Insertando datos sucios...")
            cursor.executemany(
                "INSERT INTO Panaderia.Productos VALUES (?, ?, ?, ?, ?, ?, ?)", 
                datos_para_insertar
            )
            print("Inserción completada exitosamente.")
except Exception as e:
    print(f"Error al insertar en Teradata: {e}")