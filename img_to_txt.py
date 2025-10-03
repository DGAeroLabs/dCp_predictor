# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 17:31:42 2025

@author: Aspirant2
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from scipy.ndimage import map_coordinates
import cv2

def image_to_txt(image_path, output_txt_path, original_range_min, original_range_max):
    """
    Convierte una imagen de distribución Cp normalizada de vuelta a formato .txt
    
    Parameters:
    - image_path: ruta de la imagen .png normalizada
    - output_txt_path: ruta donde guardar el archivo .txt
    - original_range_min: valor mínimo original de Cp (dcp_min global)
    - original_range_max: valor máximo original de Cp (dcp_max global)
    """
    
    # 1. Cargar la imagen
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"No se pudo cargar la imagen: {image_path}")
    
    # 2. Obtener dimensiones
    height, width = img.shape
    
    # 3. Crear matrices de coordenadas normalizadas (0 a 1)
    x_norm = np.linspace(0, 1, width)
    y_norm = np.linspace(0, 1, height)
    
    # 4. Crear malla de coordenadas
    X_norm, Y_norm = np.meshgrid(x_norm, y_norm)
    
    # 5. Convertir valores de imagen (0-255) a escala de grises normalizada (0-1)
    gray_normalized = img / 255.0  # 0=blanco, 1=Negro
    
    # 6. Invertir la escala porque en la imagen:
    #    - Blanco (255) = Cp máximo (original_range_max)
    #    - Negro (0) = Cp mínimo (original_range_min)
    cp_normalized = 1.0 - gray_normalized  # Ahora 0=Negro, 1=blanco
    
    # 7. Mapear de nuevo al rango original de Cp
    cp_values = cp_normalized * (original_range_max - original_range_min) + original_range_min
    
    # 8. Convertir a formato .txt compatible con el original
    #    Formato: X Y Cp (cada fila representa un punto)
    with open(output_txt_path, 'w') as f:
        for i in range(height):
            for j in range(width):
                x_pos = X_norm[i, j]  # Coordenada X normalizada (0-1)
                y_pos = Y_norm[i, j]  # Coordenada Y normalizada (0-1)
                cp_val = cp_values[i, j]  # Valor Cp desnormalizado
                f.write(f"{x_pos:.6f} {y_pos:.6f} {cp_val:.6f}\n")
    
    print(f"Archivo .txt generado: {output_txt_path}")
    return output_txt_path


def reconstruct_original_format_corrected(image_path, output_txt_path, 
                                        original_range_min, original_range_max, 
                                        num_sections=20, points_per_section=20):
    """
    Versión corregida: Negro = Cp mínimo, Blanco = Cp máximo
    Y invertido para coincidir con el sistema de coordenadas del ala
    """
    
    # 1. Cargar la imagen
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"No se pudo cargar la imagen: {image_path}")
    
    # 2. Convertir imagen a valores Cp (CORRECTO)
    gray_normalized = img / 255.0  # 0=blanco, 1=negro
    cp_values = gray_normalized * (original_range_max - original_range_min) + original_range_min
    
    height, width = img.shape
    
    # 3. Crear datos en el formato original (X, Y, Cp)
    reconstructed_data = []
    
    # Dividir en secciones Y
    y_sections = np.linspace(0, height-1, num_sections).astype(int)
    
    for y_idx in y_sections:
        if y_idx >= height:
            y_idx = height - 1
            
        # Extraer la fila correspondiente de Cp
        cp_row = cp_values[y_idx, :]
        
        # Tomar puntos a lo largo de X
        x_points = np.linspace(0, width-1, points_per_section).astype(int)
        
        for x_idx in x_points:
            if x_idx >= width:
                x_idx = width - 1
                
            # Convertir coordenadas normalizadas a valores (0-1)
            x_norm = x_idx / (width - 1)  # Coordenada X normalizada (0=borde ataque, 1=borde salida)
            y_norm = 1.0 - (y_idx / (height - 1))  # Coordenada Y normalizada (0=raíz, 1=punta)
            cp_val = cp_row[x_idx]  # Valor Cp en ese punto
            
            reconstructed_data.append([x_norm, y_norm, cp_val])
    
    # 4. Guardar en archivo .txt
    np.savetxt(output_txt_path, reconstructed_data, fmt='%.6f', delimiter=' ')
    print(f"Archivo .txt reconstruido correctamente: {output_txt_path}")
    return output_txt_path


def validate_conversion(original_image, reconstructed_image, original_range_min, original_range_max):
    """
    Función auxiliar para validar la conversión (opcional)
    """
    # Convertir ambas imágenes a formato comparable
    img1 = cv2.imread(original_image, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(reconstructed_image, cv2.IMREAD_GRAYSCALE)
    
    if img1.shape != img2.shape:
        print("Advertencia: Dimensiones diferentes")
        return False
    
    # Calcular diferencia
    diff = np.abs(img1.astype(float) - img2.astype(float))
    max_diff = np.max(diff)
    mean_diff = np.mean(diff)
    
    print(f"Diferencia máxima: {max_diff}")
    print(f"Diferencia media: {mean_diff}")
    
    return mean_diff < 50  # Umbral arbitrario


# Ejemplo de uso:
if __name__ == "__main__":
    # Parámetros globales (debes proporcionar los valores reales)
    dcp_min_global = -2.0885  # Ejemplo
    dcp_max_global = -0.0185  # Ejemplo
    
    # Procesar una imagen
    image_file = "0.png"  # Imagen de entrada
    output_file = "reconstructed_0.txt"  # Archivo de salida
    
    # Método 1: Simple conversión
    image_to_txt(image_file, output_file, dcp_min_global, dcp_max_global)
    
    # Método 2: Conversión más estructurada
    reconstruct_original_format_corrected(
        image_file, 
        "structured_0.txt", 
        dcp_min_global, 
        dcp_max_global,
        num_sections=20, 
        points_per_section=20
    )