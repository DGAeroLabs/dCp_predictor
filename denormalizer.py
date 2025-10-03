# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 11:18:15 2025

@author: Aspirant2
"""

import numpy as np

def denormalize_coordinates(image_txt_file, wing_config_idx, wing_configurations, output_file):
    """
    Denormaliza coordenadas de un archivo .txt generado desde imagen
    a coordenadas reales en metros basadas en la configuración original del ala
    
    Parameters:
    - image_txt_file: archivo .txt generado desde imagen (contiene X_norm, Y_norm, Cp)
    - wing_config_idx: índice de la configuración original (0, 1, 2, etc.)
    - wing_configurations: array con las configuraciones originales
    - output_file: nombre del archivo de salida con coordenadas reales
    """
    
    # Cargar configuración original
    config = wing_configurations[wing_config_idx]
    
    # Extraer parámetros (ajusta índices según tu formato real)
    wing_area = config[0]  # Área del ala
    aspect_ratio = config[1]  # Relación de aspecto
    taper_ratio = config[2]  # Razón de afilamiento (root_chord / tip_chord)
    sweep_angle = config[3]  # Ángulo de flecha
    # Ajusta según tu formato real
    
    # Calcular dimensiones reales
    span = (aspect_ratio * wing_area)**0.5  # Envergadura total
    semi_span = span / 2  # Semi-envergadura
    
    # Cuerdas (usando tus ecuaciones correctas)
    tip_chord = 2 * wing_area / (span * (1 + taper_ratio))  # Cuerda punta [m]
    root_chord = tip_chord * taper_ratio    # Cuerda raíz [m]
    
    # Cargar datos normalizados
    data = np.loadtxt(image_txt_file)
    x_norm = data[:, 0]  # Coordenadas X normalizadas (0-1)
    y_norm = data[:, 1]  # Coordenadas Y normalizadas (0-1) 
    cp_values = data[:, 2]  # Valores Cp
    
    # Convertir Y_normalizada a posición real en envergadura
    y_real = y_norm * semi_span  # Y va de 0 a semi_span
    
    # Calcular cuerda local en cada posición Y (lineal entre raíz y punta)
    local_chord = root_chord + (tip_chord - root_chord) * (y_real / semi_span)
    
    # Denormalizar coordenadas X usando la cuerda local
    x_real = x_norm * local_chord  # Ahora X varía según la cuerda local
    
    # Aplicar corrección por flecha si es necesario
    sweep_rad = np.radians(sweep_angle)
    x_real_corrected = x_real + (y_real * np.tan(sweep_rad))  # Compensar flecha
    
    # Crear archivo de salida con coordenadas reales
    denormalized_data = np.column_stack((x_real_corrected, y_real, cp_values))
    np.savetxt(output_file, denormalized_data, fmt='%.6f', delimiter=' ')
    
    print(f"Coordenadas denormalizadas guardadas en: {output_file}")
    print(f"Dimensiones del ala original:")
    print(f"  - Envergadura: {span:.3f} m")
    print(f"  - Semi-envergadura: {semi_span:.3f} m") 
    print(f"  - Cuerda raíz: {root_chord:.3f} m")
    print(f"  - Cuerda punta: {tip_chord:.3f} m")
    print(f"  - Ángulo de flecha: {sweep_angle:.2f}°")
    
    return output_file


def load_and_process_all_configurations(wing_configs_path, base_image_txt, output_dir):
    """
    Procesa todas las configuraciones para denormalizar todas las imágenes
    """
    # Cargar configuraciones
    wing_configurations = np.load(wing_configs_path)
    
    for i in range(len(wing_configurations)):
        image_txt = f"{i}.txt"  # Archivo generado desde imagen
        output_file = f"{output_dir}/{i}_denormalized.txt"
        
        try:
            denormalize_coordinates(
                image_txt, 
                i, 
                wing_configurations, 
                output_file
            )
        except FileNotFoundError:
            print(f"Archivo no encontrado: {image_txt}")
            continue


# Ejemplo de uso:
if __name__ == "__main__":
    # Cargar el array de configuraciones
    wing_configs = np.load('wing_configurations.npy')
    
    # Denormalizar una configuración específica
    denormalize_coordinates(
        'structured_0.txt',  # archivo generado desde imagen
        0,        # índice de configuración
        wing_configs,
        '0_denormalized.txt'  # salida con coordenadas reales
    )