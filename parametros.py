# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 10:01:04 2025

@author: Damian
"""
"""
wing_area = 10.0       # Wing area [m^2]
aspect_ratio = 5.0     # Aspect ratio (AR)
taper_ratio = 0.5      # Taper ratio (c_tip/c_root)
sweep_angle = 10.0     # Sweep angle [deg] (measured at leading edge)
flight_speed = 50.0    # Flight speed [m/s]
air_density = 1.225    # air density [Kg/m3]
"""
import numpy as np
from pyDOE2 import lhs
import time


def generate_configurations(n_samples=20, output_file='configurations.npy'):
    """
    Genera configuraciones aleatorias usando Latin Hypercube Sampling (LHS)
    
    Parámetros:
    n_samples (int): Número de configuraciones a generar
    output_file (str): Nombre del archivo de salida .npy
    """
    # Definición de parámetros con sus rangos
    wing_area = [5.0, 15.0]        # [m²]
    aspect_ratio = [4.0, 15.0]      # Adimensional
    taper_ratio = [1.0, 4.0]       # Adimensional
    sweep_angle = [0.0, 30.0]      # [grados]
   
    
    # Parámetros fijos
    flight_speed = 50.0            # [m/s]
    air_density = 1.204            # [kg/m³]
    num_lonzh = [1.0, 5.0]
    num_nerv = [1.0, 5.0]

    # Lista de rangos para los parámetros variables
    variable_ranges = [
        wing_area,
        aspect_ratio,
        taper_ratio,
        sweep_angle,
        num_lonzh,
        num_nerv,
    ]
    
    # Número de parámetros variables
    n_variables = len(variable_ranges)
    
    # Generar muestras LHS en el espacio [0, 1]
    samples = lhs(n_variables, samples=n_samples)
    
    # Escalar las muestras a los rangos reales
    for i in range(n_variables):
        low, high = variable_ranges[i]
        samples[:, i] = low + (high - low) * samples[:, i]
    
    # Crear matriz de parámetros fijos (repetidos para cada muestra)
    fixed_params = np.array([[flight_speed, air_density]] * n_samples)
    
    # Combinar parámetros variables y fijos
    all_configurations = np.hstack((samples, fixed_params))
    
    # Guardar en archivo .npy
    np.save(output_file, all_configurations)
    
    print(f"✅ Generadas {n_samples} configuraciones usando LHS")
    print(f"   Archivo guardado: {output_file}")
    print(f"   Dimensiones del array: {all_configurations.shape} (filas, columnas)")
    print("\nColumnas en orden:")
    print("1. Wing Area [m²]")
    print("2. Aspect Ratio")
    print("3. Taper Ratio")
    print("4. Sweep Angle [deg]")
    print("5. Flight Speed [m/s] (fijo)")
    print("6. Air Density [kg/m³] (fijo)")

inicio = time.perf_counter()
# Parámetro para controlar el número de configuraciones
NUM_CONFIGURATIONS = 10

# Generar y guardar las configuraciones
generate_configurations(
    n_samples=NUM_CONFIGURATIONS,
    output_file='wing_configurations.npy'
)

configs = np.load('wing_configurations.npy')
print(configs[0])  # Primera configuración
fin = time.perf_counter()
duracion = fin - inicio
print("\n" + "="*50)
print(f"Tiempo de ejecución: {duracion:.4f} segundos")
print("\n" + "="*50)