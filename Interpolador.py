# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 10:53:59 2025

@author: Damian
"""
import pandas as pd
import numpy as np
from scipy.interpolate import griddata


from matplotlib import cm
from matplotlib.ticker import LinearLocator

def leer_archivo(ruta):
    """Lee archivos CSV con decimales usando coma y separador de columnas por tabulador"""
    return pd.read_csv(ruta, sep='\t', decimal=',', header=0)

# Cargar datos base
base_df = leer_archivo('datos_base.txt')
# Cargar coordenadas a interpolar
target_df = leer_archivo('datos_target.txt')

# Convertir a arrays numpy
base_points = base_df[['X', 'Y']].to_numpy()
base_values = base_df['dCp'].to_numpy()
target_points = target_df[['X', 'Y']].to_numpy()

# Realizar interpolación lineal 2D
interpolated_dCp = griddata(
    points=base_points,
    values=base_values,
    xi=target_points,
    method='linear',  # Puedes cambiar a 'nearest' o 'cubic' según necesites
    fill_value=np.nan  # Para puntos fuera del convex hull
)

# Crear DataFrame con resultados
result_df = pd.DataFrame({
    'X': target_df['X'],
    'Y': target_df['Y'],
    'dCp_interpolado': interpolated_dCp
})

# Guardar resultados
result_df.to_csv('resultados_interpolacion.csv', index=False, sep='\t', decimal=',')

print("Interpolación completada. Resultados guardados en resultados_interpolacion.csv")

