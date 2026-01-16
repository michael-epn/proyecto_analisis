import pandas as pd
import sqlite3 as sql

dataset_1 = pd.read_csv("panaderia_productos.csv")
dataset_2 = pd.read_json("panaderia_productos.json")
dataset_3 = pd.read_xml("panaderia_productos.xml")
conn = sql.connect("panaderia_productos.db")
dataset_4 = pd.read_sql_query("SELECT * FROM productos_sucios", conn)
conn.close()


print("\n//////// PANADERIA_PRODUCTOS.CSV //////////////")
print(dataset_1)
print("\n//////// PANADERIA_PRODUCTOS.JSON /////////////")
print(dataset_2)
print("\n//////// PANADERIA_PRODUCTOS.XML //////////////")
print(dataset_3)
print("\n//////// PANADERIA_PRODUCTOS.DB ///////////////")
print(dataset_4)

print("/////////// DATAFRAMES CONCATENADOS ///////////////")
dataset = pd.concat([dataset_1,dataset_2,dataset_3,dataset_4], ignore_index=True)
print(" \n- Mostrar las primeras 10 filas y los tipos de datos de cada columna")
print(dataset.head(10))
print(dataset.info())

print("\n////////////// IDENTIFICANDO VALORES NULOS, VACIOS O INCORRECTOS ///////////////////")
print(dataset.isnull().sum())

print("\n############ CALCULANDO EL PORCENTAJE DE DATOS SUCIOS EN CADA COLUMNA ###########")
total = len(dataset)
nulos = dataset.isnull().sum()
porcentaje = (nulos / total) * 100
print(porcentaje.round(2).astype(str) + " %")

print("///////////// IDENTIFICANDO DUPLICADOS ////////////////")
print(dataset.duplicated().sum())
print("//////////// VALORES FUERA DE DOMINIO //////////////////")
print(dataset["stock"].unique())
print("//////////// STRING SUCIOS //////////////////////")
#Aqui se puede ir cambiando el nombre de la columna, o sino le puedes hacer para todas las columnas
print("Nombre = ",dataset["nombre"].str.contains(" ",regex = False).sum())
print("Categoria = ",dataset["categoria"].str.contains(" ",regex = False).sum())
print("Stock = ",dataset["stock"].str.contains(" ",regex = False).sum())
print("Proveedor = ",dataset["proveedor"].str.contains(" ",regex = False).sum())
print("Precio de compra = ",dataset["precio_compra"].str.contains(" ",regex = False).sum())
print("Precio de venta al publico = ",dataset["precio_venta_publico"].str.contains(" ",regex = False).sum())

######################################################################################################################################
dataset_limpio = dataset.copy()
print("//////////// LIMPIANDO EL DATASET ///////////////////")
print("1. Limpiar columnas numéricas...")
columnas_numericas = ["precio_compra", "precio_venta_publico", "stock"]

for col in columnas_numericas:
    dataset_limpio[col] = pd.to_numeric(dataset_limpio[col], errors="coerce")

print("2. Rellenar valores nulos con la mefianam y las tipo string con desconocido...")
for col in columnas_numericas:
    dataset_limpio[col].fillna(dataset_limpio[col].median(), inplace=True)

columnas_texto = ["nombre", "categoria", "proveedor"]

for col in columnas_texto:
    dataset_limpio[col].fillna("Desconocido", inplace=True)

print("3. Limpiar espacios y estandarizar texto...")
for col in columnas_texto:
    dataset_limpio[col] = dataset_limpio[col].str.strip()

print("4. Validar dominio de stock...")
dataset_limpio = dataset_limpio[dataset_limpio["stock"] >= 0]

print("5. Revisar tipos de datos finales...")
print(dataset_limpio.info())

print("6. Verificar que ya no hay datos sucios...")
print(dataset_limpio.isnull().sum())
########################################################################################################################################
