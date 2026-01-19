import pandas as pd
import random
import sys

sys.stdout.reconfigure(encoding='utf-8')

def generar_dataset_insumos(id_range):
    catalogo_insumos = {
        "Quintal Harina Trigo": {"base": 45.00, "cat": "Materia Prima", "provs": ["Moderna", "Santa Lucia"]},
        "Litro Leche Entera": {"base": 0.90, "cat": "Lácteos", "provs": ["Vita", "Rey Leche"]},
        "Cubeta Huevos (30u)": {"base": 3.50, "cat": "Materia Prima", "provs": ["Indaves", "Avícola"]},
        "Margarina Industrial": {"base": 2.50, "cat": "Grasas", "provs": ["Danec", "La Fabril"]},
        "Esencia Vainilla (Galón)": {"base": 12.00, "cat": "Esencias", "provs": ["DelyClar"]},
        "Chocolate Cobertura (Kg)": {"base": 8.50, "cat": "Repostería", "provs": ["DelyClar", "Pacari"]},
        "Levadura Fresca (500g)": {"base": 2.25, "cat": "Materia Prima", "provs": ["Levapan"]}
    }
    
    items = list(catalogo_insumos.keys())
    data = []

    for i in id_range:
        nombre_item = random.choice(items)
        info = catalogo_insumos[nombre_item]
        
        variacion = random.uniform(-0.05, 0.05)
        precio_real = round(info["base"] * (1 + variacion), 2)

        row = {
            "id_insumo": i,
            "nombre": nombre_item,
            "precio_compra": str(precio_real),
            "categoria": info["cat"],
            "stock": str(random.randint(0, 500)),
            "proveedor": random.choice(info["provs"]),
        }
        
        if random.random() < 0.45:
            campo = random.choice(["stock", "proveedor", "categoria", "precio_compra"])
            row[campo] = random.choice(["error", "N/A", "", "texto_random", "NaN"])
            
        data.append(row)
    return pd.DataFrame(data)


df_csv = generar_dataset_insumos(range(1, 100))
df_json = generar_dataset_insumos(range(100, 200))
df_xml = generar_dataset_insumos(range(200, 300))
df_db = generar_dataset_insumos(range(300, 400))

df_csv.to_csv('insumos_panaderia.csv', index=False)
df_json.to_json('insumos_panaderia.json', orient='records', indent=4)
df_xml.to_xml('insumos_panaderia.xml', index=False)
df_db.to_sql('insumos_sucios', 'sqlite:///panaderia_insumos.db', if_exists='replace', index=False)