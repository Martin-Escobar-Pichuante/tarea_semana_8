import os
import pandas as pd
import numpy as np

def procesar_datos_aqualimpia(ruta_archivo):
    print("=== Iniciando Procesamiento Analítico - AquaLimpia S.A. ===")
    
    # 1. Carga de datos
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")
    
    df = pd.read_excel(ruta_archivo)
    
    # 2. Conversión de tipos y limpieza básica
    df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
    
    # 3. Ingeniería de Características (Feature Engineering) con NumPy
    # Calculamos la eficiencia de remoción de DBO
    df['eficiencia_remocion_DBO'] = np.round(
        ((df['DBO_entrada_mg_L'] - df['DBO_salida_mg_L']) / df['DBO_entrada_mg_L']) * 100, 
        2
    )
    
    print("\n--- Resumen Estadístico de Incumplimientos por Planta ---")
    resumen = df.groupby('planta').agg(
        total_registros=('cumplimiento_norma', 'count'),
        incumplimientos=('cumplimiento_norma', lambda x: (x == 0).sum()),
        tasa_incumplimiento_pct=('cumplimiento_norma', lambda x: np.round((x == 0).mean() * 100, 2)),
        eficiencia_promedio_pct=('eficiencia_remocion_DBO', 'mean')
    )
    print(resumen)
    
    # 4. Generación de archivos de salida para áreas específicas
    os.makedirs("data/processed", exist_ok=True)
    
    # Salida Área de Operaciones
    cols_operaciones = [
        'fecha_registro', 'planta', 'caudal_entrada_m3_d', 
        'DBO_entrada_mg_L', 'DBO_salida_mg_L', 'eficiencia_remocion_DBO',
        'energia_aeracion_kWh', 'lodos_generados_kg_d'
    ]
    df_operaciones = df[cols_operaciones]
    df_operaciones.to_csv("data/processed/reporte_operaciones.csv", index=False)
    
    # Salida Área de Gestión Ambiental
    cols_ambiental = [
        'fecha_registro', 'planta', 'DBO_salida_mg_L', 'cumplimiento_norma'
    ]
    df_ambiental = df[cols_ambiental]
    df_ambiental.to_csv("data/processed/reporte_gestion_ambiental.csv", index=False)
    
    print("\n[ÉXITO] Archivos para Operaciones y Gestión Ambiental generados con éxito.")
    return df

if __name__ == "__main__":
    # Nombre del archivo basado en tu dataset cargado
    ruta_datos = r"C:\Users\vllhcontrol19\Desktop\dataset.xlsx"
    df_procesado = procesar_datos_aqualimpia(ruta_datos)