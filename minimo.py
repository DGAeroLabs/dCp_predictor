# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 14:57:38 2025

@author: Aspirant2
"""
import numpy as np

def find_min_dcp(file, all_min):
    """
    Analiza el archivo '0.txt' y encuentra el valor mínimo en la tercera columna.
    
    Returns:
        float: El valor mínimo encontrado en la tercera columna
    """
    min_value = all_min # Inicializar con infinito para asegurar que cualquier número será menor
    
    try:
        with open(f'{file}', 'r') as file:
            for line in file:
                # Saltar líneas vacías
                if not line.strip():
                    continue
                
                # Dividir por tabulaciones y limpiar espacios
                columns = line.strip().split('\t')
                
                # Verificar que tenga al menos 3 columnas
                if len(columns) >= 3:
                    try:
                        # Convertir la tercera columna a float
                        dcp_value = float(columns[2])
                        
                        # Actualizar el mínimo si encontramos un valor menor
                        if dcp_value < min_value:
                            min_value = dcp_value
                    except ValueError:
                        # Ignorar líneas con valores no numéricos en la tercera columna
                        continue
    
    except FileNotFoundError:
        print("Error: El archivo '0.txt' no se encontró en el directorio actual.")
        return None
    
    # Si no se encontró ningún valor válido
    if min_value == float('inf'):
        print("Advertencia: No se encontraron valores numéricos válidos en la tercera columna.")
        return None
    
    return min_value

def find_max_dcp(file, all_max):
    """
    Analiza el archivo '0.txt' y encuentra el valor mínimo en la tercera columna.
    
    Returns:
        float: El valor mínimo encontrado en la tercera columna
    """
    max_value = all_max  # Inicializar con menos infinito para asegurar que cualquier número será mayor
    
    try:
        with open(f'{file}', 'r') as file:
            for line in file:
                # Saltar líneas vacías
                if not line.strip():
                    continue
                
                # Dividir por tabulaciones y limpiar espacios
                columns = line.strip().split('\t')
                
                # Verificar que tenga al menos 3 columnas
                if len(columns) >= 3:
                    try:
                        # Convertir la tercera columna a float
                        dcp_value = float(columns[2])
                        
                        # Actualizar el mínimo si encontramos un valor menor
                        if dcp_value > max_value:
                            max_value = dcp_value
                    except ValueError:
                        # Ignorar líneas con valores no numéricos en la tercera columna
                        continue
    
    except FileNotFoundError:
        print("Error: El archivo '0.txt' no se encontró en el directorio actual.")
        return None
    
    # Si no se encontró ningún valor válido
    if max_value == float('-inf'):
        print("Advertencia: No se encontraron valores numéricos válidos en la tercera columna.")
        return None
    
    return max_value
'''
configurations = np.load('wing_configurations.npy')

all_min = float('inf')                              #encontrar el minimo total
for idx, config in enumerate(configurations):
    input_filename = f"{idx}.txt"
    dcp_min = find_min_dcp(input_filename, all_min)
    if dcp_min < all_min:
        all_min=dcp_min
        print(f" new minimum in {input_filename}")
        
all_max = float('-inf')                            #encontrar el minimo total
for idx, config in enumerate(configurations):
    input_filename = f"{idx}.txt"
    dcp_max = find_max_dcp(input_filename, all_max)
    if dcp_max > all_max:
        all_max = dcp_max
        print(f" new maximum in {input_filename}")
'''