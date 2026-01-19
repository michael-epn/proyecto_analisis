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
    host = '192.168.100.27'
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

print("\n############ 1. IDENTIFICAR VALORES NULOS ###########")
print(df.isnull().sum())

print("\n###### 2. CONVERTIR TIPOS DE DATOS (precio_compra, stock) ###########")
df["precio_compra"] = pd.to_numeric(df["precio_compra"], errors="coerce")
df["stock"] = pd.to_numeric(df["stock"], errors="coerce")


df.info()

print("\n############ 3. IMPUTAR VALORES FALTANTES ###########")

mediana_precio = df["precio_compra"].median()
df["precio_compra"] = df["precio_compra"].fillna(mediana_precio)


valores_incorrectos = ["error", "N/A", "", "texto_random", "NaN", "null", "NULL"]

df["categoria"] = df["categoria"].fillna("Sin categoría")

df.loc[df['categoria'].isin(valores_incorrectos), 'categoria'] = 'Sin categoría'

df["proveedor"] = df["proveedor"].fillna("Proveedor X")

df.loc[df['proveedor'].isin(valores_incorrectos), 'proveedor'] = 'Proveedor X'


df["nombre"] = df["nombre"].fillna("Desconocido")
df["stock"] = df["stock"].fillna(0)

print("Limpieza completada.")

print("COMPROBANDO LIMPIEZA:\n")
print("ANTES")
print(df_unificado.isnull().sum())
print("\nDESPUÉS")
print(df.isnull().sum())

print("\n############ 4. VALIDACIÓN LÓGICA ###########")
print("\nStock negativo:")
print(df[df['stock'] < 0])

print("\nEliminar Duplicados por ID")
df = df.drop_duplicates(subset=['id_insumo'], keep='first')
print(f"Registros restantes tras eliminar duplicados: {len(df)}")

print("\n############ 5. ESTADÍSTICAS DESCRIPTIVAS ###########")
for col in ['precio_compra', 'stock']:
    print(f"\nEstadísticas para {col}:")
    print(f"Mínimo: {df[col].min()}")
    print(f"Máximo: {df[col].max()}")
    print(f"Media: {df[col].mean():.2f}")
    print(f"Mediana: {df[col].median():.2f}")
    print(f"Desviación estándar: {df[col].std():.2f}")

print("\n############ 6. IDENTIFICAR OUTLIERS (Valores Extremos) ###########")
for col in ['precio_compra', 'stock']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    outliers = df[(df[col] < limite_inferior) | (df[col] > limite_superior)]
    print(f"\nOutliers detectados en {col} (Total: {len(outliers)}):")
    if not outliers.empty:
        print(outliers[['id_insumo', 'nombre', col]].head())

print("\n############ 7. ANÁLISIS POR CATEGORÍA ###########")

print("\n--- Conteo de insumos únicos por categoría ---")
insumos_por_categoria = df.groupby('categoria')['id_insumo'].nunique().sort_values(ascending=False)
print(insumos_por_categoria)

print("\n--- Stock Total e Inversión (Estimada) por Categoría ---")
df['valor_inventario'] = df['precio_compra'] * df['stock']

resumen_categoria = df.groupby('categoria').agg({
    'stock': 'sum',
    'precio_compra': 'mean',
    'valor_inventario': 'sum'
}).sort_values('stock', ascending=False)

resumen_categoria.rename(columns={'precio_compra': 'precio_compra_promedio'}, inplace=True)
print(resumen_categoria)


print("\n############ 8. TOP insumos ###########")
print("\n--- Top 5 insumos con Mayor Stock ---")
top10_stock = df.sort_values('stock', ascending=False).head(10)
print(top10_stock[['id_insumo', 'nombre', 'categoria', 'proveedor', 'stock']])

print("\n--- Top 5 insumos más Costosos (Precio Compra) ---")
top10_costosos = df.sort_values('precio_compra', ascending=False).head(10)
print(top10_costosos[['id_insumo', 'nombre', 'categoria', 'proveedor', 'precio_compra']])


stock_real = df.groupby('nombre')['stock'].sum().sort_values(ascending=False)

print("\n--- STOCK REAL TOTAL (Agrupado) ---")
print(stock_real.head(10))

################################### VISUALIZACIÓN ######################################

sns.set_theme(style="whitegrid")

plt.figure(figsize=(8, 5))
sns.histplot(df['precio_compra'], bins=20, kde=True, color='skyblue')
plt.title('Distribución de Precios de Compra')
plt.xlabel('Precio de Compra ($)')
plt.ylabel('Frecuencia')
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x='categoria', y='stock', hue='categoria', legend=False, data=resumen_categoria.reset_index(), palette='viridis')
plt.xticks(rotation=45)
plt.title('Stock Total por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Stock')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x='categoria', y='precio_compra', hue='categoria', legend=False, data=df, palette='pastel')
plt.xticks(rotation=45)
plt.title('Variabilidad de Precios de Compra por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Precio de Compra')
plt.tight_layout()
plt.show()

conteo_categorias = df['categoria'].value_counts()

plt.figure(figsize=(7, 7))
colores = sns.color_palette('pastel', n_colors=len(conteo_categorias))

plt.pie(conteo_categorias, 
        labels=conteo_categorias.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colores)

plt.title('Distribución de Insumos por Categoría')
plt.show()