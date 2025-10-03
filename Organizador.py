# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 00:09:48 2025

@author: Damian
"""

import re
import csv
from collections import defaultdict

def process_cp_data(input_file, output_pivot, output_columns):
    # Diccionarios para almacenar los datos
    data = defaultdict(dict)
    all_data = []
    y_values = set()
    x_values = set()
    current_y = None
    
    # Expresiones regulares para buscar los valores
    y_pattern = re.compile(r'BLOCK Cut_\d+_at_Y:_([\d.]+)')
    data_pattern = re.compile(r'\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)')

    with open(input_file, 'r') as f:
        for line in f:
            # Buscar coordenada Y del bloque
            y_match = y_pattern.match(line)
            if y_match:
                current_y = round(float(y_match.group(1)), 4)
                y_values.add(current_y)
                continue
            
            # Buscar líneas de datos
            data_match = data_pattern.match(line)
            if data_match and current_y is not None:
                x = round(float(data_match.group(1)), 4)
                y = round(float(data_match.group(2)), 4)
                cp = float(data_match.group(4))
                
                # Almacenar para tabla pivot
                x_values.add(x)
                data[x][current_y] = cp
                
                # Almacenar para archivo de columnas
                all_data.append((x, current_y, cp))

    # Generar archivo pivot ********************************
    sorted_y = sorted(y_values)
    sorted_x = sorted(x_values, reverse=True)

    # Crear la tabla pivot
    pivot_table = []
    header = ['X/Y'] + [f"{y:.4f}" for y in sorted_y]
    pivot_table.append(header)
    
    for x in sorted_x:
        row = [f"{x:.4f}"]
        for y in sorted_y:
            value = data[x].get(y, None)
            row.append(f"{value:.4f}" if value is not None else '')
        pivot_table.append(row)

    # Escribir archivo pivot CSV
    with open(output_pivot, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(pivot_table)
    
    # Generar archivo de columnas CORREGIDO **************************
    # Crear un diccionario para almacenar puntos únicos por (X,Y)
    unique_points = {}
    
    # Extraer puntos únicos del diccionario data
    for x in x_values:
        for y in y_values:
            if y in data[x]:
                # Usamos (x, y) como clave única
                unique_points[(x, y)] = data[x][y]
    
    # Convertir a lista y ordenar por Y y luego por X (de mayor a menor)
    sorted_unique_data = sorted(
        [(x, y, cp) for (x, y), cp in unique_points.items()],
        key=lambda d: (d[1], -d[0])
    )
    
    # Escribir archivo de columnas TSV (usando tabulaciones)
    with open(output_columns, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        
        for x, y, cp in sorted_unique_data:
            writer.writerow([f"{x:.4f}", f"{y:.4f}", f"{cp:.4f}"])

    print(f"Archivos generados exitosamente:")
    print(f"- Tabla pivot: {output_pivot}")
    print(f"- Datos en columnas: {output_columns}")

'''
# Uso del script
input_filename = "0.slc"
output_pivot = "tabla_pivot.csv"
output_columns = "datos_base.txt"

process_cp_data(input_filename, output_pivot, output_columns)
'''