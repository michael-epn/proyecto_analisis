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


