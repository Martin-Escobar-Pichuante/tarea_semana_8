import pandas as pd
import numpy as np
import os

def inicializar_proyecto_aqualimpia(ruta_excel):
    """
    Carga el dataset de AquaLimpia S.A., limpia los nombres de las columnas
    y verifica su carga correcta en memoria.
    """
    if not os.path.exists(ruta_excel):
        raise FileNotFoundError(f"No se encontró el archivo de datos en: {ruta_excel}")
        
    # Carga del set de datos
    df = pd.read_excel(ruta_excel)
    
    # Estandarización de nombres de columnas a minúsculas y sin espacios problemáticos
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    print(f"--- Dataset AquaLimpia S.A. Cargado Correctamente ---")
    print(f"Total de registros evaluados: {df.shape[0]}")
    print(f"Columnas identificadas: {list(df.columns)}\n")
    
    return df

# Suponiendo la ubicación estándar en el entorno de trabajo
ruta_datos = r"C:\Users\vllhcontrol19\Desktop\dataset.xlsx"
try:
    df_aguas = inicializar_proyecto_aqualimpia(ruta_datos)
except Exception as e:
    print(f"Nota de desarrollo: Configure la ruta correcta del archivo Excel. Error: {e}")