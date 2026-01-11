import pandas as pd
import numpy as np
import random
import sys
sys.stdout.reconfigure(encoding='utf-8')

def generar_dataset_sucio(id_range):
    productos = ["Pan de Masa Madre", "Pastel de Chocolate", "Pan de Leche", "Galletas", "Cacho", "Gusano", "Donas"]
    categorias = ["Panadería", "Pastelería", "Insumos", "Cafetería"]
    proveedores = ["Moderna", "Vita", "DelyClar"]
    
    data = []
    for i in id_range:
        pc = round(random.uniform(0.5, 20.0), 2)
        row = {
            "id": i,
            "nombre": random.choice(productos),
            "precio_compra": str(pc),
            "categoria": random.choice(categorias),
            "stock": str(random.randint(0, 300)),
            "proveedor": random.choice(proveedores),
            "precio_venta_publico": str(round(pc * 1.5, 2))
        }
        
        if random.random() < 0.25:
            campo = random.choice(["precio_compra", "stock", "proveedor", "precio_venta_publico", "nombre", "categoria"])
            row[campo] = random.choice(["error", "N/A", "", "texto", "NaN"])
            
        data.append(row)
    return pd.DataFrame(data)

df_csv = generar_dataset_sucio(range(1, 100))
df_json = generar_dataset_sucio(range(100, 200))
df_xml = generar_dataset_sucio(range(200, 300))
df_db = generar_dataset_sucio(range(300, 400))


df_csv.to_csv('panaderia_productos.csv', index=False)
df_json.to_json('panaderia_productos.json', orient='records', indent=4)
df_xml.to_xml('panaderia_productos.xml', index=False)
df_db.to_sql('productos_sucios', 'sqlite:///panaderia_productos.db', if_exists='replace', index=False)

print("Archivos generados exitosamente.")