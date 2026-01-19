from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Importante: Modo "sin ventanas" para servidores web
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

from logica_negocio import obtener_datos_procesados

app = Flask(__name__)

def crear_grafico():
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

@app.route('/')
def dashboard():
    df = obtener_datos_procesados()
    
    estilos_tabla = 'table table-striped table-hover table-bordered text-center align-middle'
    
    top_stock = df.sort_values('stock', ascending=False).head(10)
    tabla_stock = top_stock[['id_insumo', 'nombre', 'categoria', 'stock']].to_html(classes='table table-striped table-hover', index=False)

    top_costos = df.sort_values('precio_compra', ascending=False).head(10)
    tabla_costos = top_costos[['id_insumo', 'nombre', 'categoria', 'precio_compra']].to_html(classes='table table-striped table-hover', index=False)
    
    total_items = len(df)
    valor_total_inventario = (df['precio_compra'] * df['stock']).sum()
    categoria_top = df['categoria'].mode()[0]
    
    stock_critico = df[(df['stock'] < 20) & (df['stock'] > 0)].sort_values('stock', ascending=True).head(5)
    tabla_alertas = stock_critico[['id_insumo', 'nombre', 'stock', 'proveedor']].to_html(classes='table table-danger table-hover', index=False)
    cantidad_alertas = len(df[df['stock'] < 20])

    top_proveedores = df['proveedor'].value_counts().head(5).reset_index()
    top_proveedores.columns = ['Proveedor', 'Cant. Productos']
    tabla_proveedores = top_proveedores.to_html(classes='table table-bordered', index=False)

    df['valor_total_linea'] = df['precio_compra'] * df['stock']
    valor_por_cat = df.groupby('categoria')['valor_total_linea'].sum().sort_values(ascending=False).reset_index()
    data_agrupada = df.groupby('categoria')['stock'].sum().reset_index().sort_values('stock', ascending=False)

    # --- GRÁFICOS ---
    plt.figure(figsize=(10, 6))
    sns.barplot(x='categoria', y='stock', hue='categoria', data=data_agrupada, palette='viridis', legend=False)
    plt.title('Stock Total por Categoría')
    plt.xlabel('Categoría')
    plt.ylabel('Stock')
    plt.xticks(rotation=45)
    grafico_barras = crear_grafico()

    conteo_categorias = df['categoria'].value_counts()
    plt.figure(figsize=(10, 3.14))
    colores = sns.color_palette('pastel', n_colors=len(conteo_categorias))
    plt.pie(conteo_categorias, labels=conteo_categorias.index, autopct='%1.1f%%', startangle=140, colors=colores)
    plt.title('Distribución de Insumos por Categoría')
    grafico_pastel = crear_grafico()

    plt.figure(figsize=(10, 6.65))
    sns.histplot(df['precio_compra'], bins=20, kde=True, color='skyblue')
    plt.title('Distribución de Precios de Compra')
    plt.xlabel('Precio de Compra ($)')
    plt.ylabel('Frecuencia')
    grafico_hist = crear_grafico()
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='categoria', y='precio_compra', hue='categoria', legend=False, data=df, palette='pastel')
    plt.xticks(rotation=45)
    plt.title('Variabilidad de Precios de Compra por Categoría')
    plt.xlabel('Categoría')
    plt.ylabel('Precio de Compra')
    grafico_box = crear_grafico()
    
    plt.figure(figsize=(10, 6))
    plt.pie(valor_por_cat['valor_total_linea'], labels=valor_por_cat['categoria'], autopct='%1.1f%%', pctdistance=0.85, colors=sns.color_palette('Set2'))
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title('Valor Monetario ($) por Categoría')
    grafico_dinero = crear_grafico()

    return render_template('dashboard.html', 
                           tabla_stock=tabla_stock,
                           tabla_costos=tabla_costos,
                           grafico_barras=grafico_barras,
                           grafico_pastel=grafico_pastel,
                           tabla_alertas=tabla_alertas,
                           tabla_proveedores=tabla_proveedores,
                           cantidad_alertas=cantidad_alertas,
                           grafico_hist=grafico_hist,
                           grafico_box=grafico_box,
                           grafico_dinero=grafico_dinero,
                           total_items=total_items,
                           valor_total=round(valor_total_inventario, 2),
                           cat_top=categoria_top)

if __name__ == '__main__':
    app.run(debug=True, port=5000)