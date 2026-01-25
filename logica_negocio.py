import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import sys
sys.stdout.reconfigure(encoding='utf-8')
def obtener_datos_procesados():
    try:
        df2 = pd.read_json("datos/insumos_panaderia.json")
        df3 = pd.read_xml("datos/insumos_panaderia.xml")
        df1 = pd.read_csv("datos/insumos_panaderia.csv")
        
        conn = sqlite3.connect("datos/panaderia_insumos.db")
        df4 = pd.read_sql_query("SELECT * FROM insumos_sucios", conn)
        conn.close()
    except FileNotFoundError as e:
        print(e)
        
    try:
        user = 'dbc'
        pasw = 'dbc'
        host = '192.168.100.25'
        engine_string = f'teradatasql://{user}:{pasw}@{host}'
        engine = create_engine(engine_string)
        query = "SELECT id_insumo, nombre, precio_compra FROM Panaderia.Insumos"
        df5 = pd.read_sql(query, engine)
    except Exception as e:
        print(e)

    load_dotenv()
    uri = "mongodb+srv://maykolaicogg3_db_user:KrwVu5AGD1wtGizL@datos.wrq4154.mongodb.net/?appName=Datos"

    try:
        with MongoClient(uri) as client:
            filtro_query = {} 
            columnas_select = {
                "_id": 0, 
                "id_insumo": 1, 
                "nombre": 1, 
                "precio_compra": 1, 
                "categoria": 1, 
                "stock": 1, 
                "proveedor": 1, 
            }
            cursor = client["Panaderia"]["Insumos"].find(filtro_query, columnas_select)
            df6 = pd.DataFrame(list(cursor))
    except Exception as e:
        print(e)

    df_unificado = pd.concat([df1, df2, df3, df4, df5, df6], ignore_index=True)
    df = df_unificado.copy()
    
    df["precio_compra"] = pd.to_numeric(df["precio_compra"], errors="coerce")
    df["stock"] = pd.to_numeric(df["stock"], errors="coerce")
    mediana_precio = df["precio_compra"].median()
    df["precio_compra"] = df["precio_compra"].fillna(mediana_precio)
    
    valores_incorrectos = ["error", "N/A", "", "texto_random", "NaN", "null", "NULL"]

    df["categoria"] = df["categoria"].fillna("Sin categoría")
    df.loc[df['categoria'].isin(valores_incorrectos), 'categoria'] = 'Sin categoría'

    df["proveedor"] = df["proveedor"].fillna("Proveedor X")
    df.loc[df['proveedor'].isin(valores_incorrectos), 'proveedor'] = 'Proveedor X'

    df["nombre"] = df["nombre"].fillna("Desconocido")
    df["stock"] = df["stock"].fillna(0)
    df = df.drop_duplicates(subset=['id_insumo'], keep='first')
    return df