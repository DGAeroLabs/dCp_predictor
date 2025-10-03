# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 11:23:27 2025

@author: Aspirant2
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_two_surfaces_3d_formatted(file1_path, file2_path, title="Comparación 3D", 
                                  label1="Superficie 1", label2="Superficie 2",
                                  cmap1='viridis', cmap2='plasma'):
    """
    Dibuja dos superficies 3D a partir de archivos .txt con formato:
    X Y Cp (cada fila representa un punto en la superficie del ala)
    
    Parameters:
    - file1_path, file2_path: rutas de los archivos .txt
    - title: título del gráfico
    - label1, label2: etiquetas para las superficies
    - cmap1, cmap2: mapas de color para cada superficie
    """
    
    # Cargar datos
    data1 = np.loadtxt(file1_path)
    data2 = np.loadtxt(file2_path)
    
    # Extraer coordenadas
    x1, y1, z1 = data1[:, 0], data1[:, 1], data1[:, 2]  # X Y Cp
    x2, y2, z2 = data2[:, 0], data2[:, 1], data2[:, 2]  # X Y Cp
    
    # Crear mallas regulares para superficies
    # Obtener valores únicos de X e Y
    x1_unique = np.unique(x1)
    y1_unique = np.unique(y1)
    x2_unique = np.unique(x2)
    y2_unique = np.unique(y2)
    
    # Crear matrices de malla
    X1_mesh, Y1_mesh = np.meshgrid(x1_unique, y1_unique)
    X2_mesh, Y2_mesh = np.meshgrid(x2_unique, y2_unique)
    
    # Crear matrices Z interpoladas
    Z1 = np.full_like(X1_mesh, np.nan)
    Z2 = np.full_like(X2_mesh, np.nan)
    
    # Mapear valores Z a las matrices de malla
    for i, y_val in enumerate(y1_unique):
        for j, x_val in enumerate(x1_unique):
            mask = (x1 == x_val) & (y1 == y_val)
            if np.any(mask):
                Z1[i, j] = z1[mask][0]  # Tomar primer valor encontrado
    
    for i, y_val in enumerate(y2_unique):
        for j, x_val in enumerate(x2_unique):
            mask = (x2 == x_val) & (y2 == y_val)
            if np.any(mask):
                Z2[i, j] = z2[mask][0]  # Tomar primer valor encontrado
    
    # Crear figura 3D
    fig = plt.figure(figsize=(15, 5))
    
    # Subplot 1: Ambas superficies en el mismo gráfico
    ax1 = fig.add_subplot(131, projection='3d')
    surf1 = ax1.plot_surface(X1_mesh, Y1_mesh, Z1, alpha=0.6, cmap=cmap1, label=label1)
    surf2 = ax1.plot_surface(X2_mesh, Y2_mesh, Z2, alpha=0.6, cmap=cmap2, label=label2)
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Cp')
    ax1.set_title(f'{title} - Superposición')
    
    # Subplot 2: Superficie 1 sola
    ax2 = fig.add_subplot(132, projection='3d')
    surf1_only = ax2.plot_surface(X1_mesh, Y1_mesh, Z1, alpha=0.8, cmap=cmap1)
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.set_zlabel('Cp')
    ax2.set_title(f'{label1}')
    
    # Subplot 3: Superficie 2 sola
    ax3 = fig.add_subplot(133, projection='3d')
    surf2_only = ax3.plot_surface(X2_mesh, Y2_mesh, Z2, alpha=0.8, cmap=cmap2)
    ax3.set_xlabel('X (m)')
    ax3.set_ylabel('Y (m)')
    ax3.set_zlabel('Cp')
    ax3.set_title(f'{label2}')
    
    plt.tight_layout()
    plt.show()
    
    return fig


def plot_two_surfaces_scatter(file1_path, file2_path, title="Comparación 3D", 
                             label1="Superficie 1", label2="Superficie 2"):
    """
    Versión con scatter plots para datos dispersos
    """
    
    # Cargar datos
    data1 = np.loadtxt(file1_path)
    data2 = np.loadtxt(file2_path)
    
    # Extraer coordenadas
    x1, y1, z1 = data1[:, 0], data1[:, 1], data1[:, 2]
    x2, y2, z2 = data2[:, 0], data2[:, 1], data2[:, 2]
    
    # Crear figura
    fig = plt.figure(figsize=(12, 4))
    
    # Subplot 1: Ambas superficies como scatter
    ax1 = fig.add_subplot(131, projection='3d')
    scatter1 = ax1.scatter(x1, y1, z1, c=z1, cmap='viridis', alpha=0.6, label=label1)
    scatter2 = ax1.scatter(x2, y2, z2, c=z2, cmap='plasma', alpha=0.6, label=label2)
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Cp')
    ax1.set_title(f'{title} - Scatter')
    plt.colorbar(scatter1, ax=ax1, shrink=0.5, aspect=10)
    
    # Subplot 2: Superficie 1
    ax2 = fig.add_subplot(132, projection='3d')
    scatter1_only = ax2.scatter(x1, y1, z1, c=z1, cmap='viridis', alpha=0.8)
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.set_zlabel('Cp')
    ax2.set_title(f'{label1}')
    plt.colorbar(scatter1_only, ax=ax2, shrink=0.5, aspect=10)
    
    # Subplot 3: Superficie 2
    ax3 = fig.add_subplot(133, projection='3d')
    scatter2_only = ax3.scatter(x2, y2, z2, c=z2, cmap='plasma', alpha=0.8)
    ax3.set_xlabel('X (m)')
    ax3.set_ylabel('Y (m)')
    ax3.set_zlabel('Cp')
    ax3.set_title(f'{label2}')
    plt.colorbar(scatter2_only, ax=ax3, shrink=0.5, aspect=10)
    
    plt.tight_layout()
    plt.show()
    
    return fig


def compare_cp_distributions(file1_path, file2_path, title="Comparación Cp"):
    """
    Comparación adicional de distribuciones Cp
    """
    
    data1 = np.loadtxt(file1_path)
    data2 = np.loadtxt(file2_path)
    
    z1 = data1[:, 2]  # Cp valores
    z2 = data2[:, 2]  # Cp valores
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Histogramas
    axes[0,0].hist(z1, bins=50, alpha=0.7, label='Superficie 1', density=True)
    axes[0,0].hist(z2, bins=50, alpha=0.7, label='Superficie 2', density=True)
    axes[0,0].set_title('Distribución Cp')
    axes[0,0].legend()
    axes[0,0].set_xlabel('Cp')
    axes[0,0].set_ylabel('Densidad')
    
    # Comparación de valores
    axes[0,1].scatter(range(len(z1)), z1, alpha=0.6, label='Superficie 1', s=1)
    axes[0,1].scatter(range(len(z2)), z2, alpha=0.6, label='Superficie 2', s=1)
    axes[0,1].set_title('Serie temporal Cp')
    axes[0,1].legend()
    axes[0,1].set_xlabel('Índice')
    axes[0,1].set_ylabel('Cp')
    
    # Estadísticas
    stats_data = [
        [np.min(z1), np.max(z1), np.mean(z1), np.std(z1)],
        [np.min(z2), np.max(z2), np.mean(z2), np.std(z2)]
    ]
    
    import pandas as pd
    stats_df = pd.DataFrame(stats_data, 
                           columns=['Mínimo', 'Máximo', 'Media', 'Std'], 
                           index=['Superficie 1', 'Superficie 2'])
    
    # Mostrar tabla de estadísticas
    axes[1,0].axis('tight')
    axes[1,0].axis('off')
    table = axes[1,0].table(cellText=stats_df.values,
                           colLabels=stats_df.columns,
                           rowLabels=stats_df.index,
                           cellLoc='center',
                           loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    axes[1,0].set_title('Estadísticas Cp')
    
    # Diferencia absoluta
    min_len = min(len(z1), len(z2))
    z1_trimmed = z1[:min_len]
    z2_trimmed = z2[:min_len]
    diff = np.abs(z1_trimmed - z2_trimmed)
    
    axes[1,1].plot(diff, alpha=0.7)
    axes[1,1].set_title('Diferencia absoluta Cp')
    axes[1,1].set_xlabel('Índice')
    axes[1,1].set_ylabel('|Cp1 - Cp2|')
    
    plt.tight_layout()
    plt.show()
    
    return fig, stats_df


# Ejemplo de uso:
if __name__ == "__main__":
    # Dibujar superficies
    fig1 = plot_two_surfaces_3d_formatted(
        '0.txt',      # archivo de ejemplo 1
        '0_denormalized.txt',      # archivo de ejemplo 2
        title="Comparación Distribución Cp",
        label1="Ala A",
        label2="Ala B"
    )
    
    # Alternativamente, usar scatter para datos dispersos
    fig2 = plot_two_surfaces_scatter(
        '0.txt',
        '0_denormalized.txt',
        title="Comparación Cp 3D",
        label1="Ala A", 
        label2="Ala B"
    )
    
    # Comparación estadística
    fig3, stats = compare_cp_distributions(
        '0.txt',
        '0_denormalized.txt',
        title="Comparación Estadística Cp"
    )
    
    print("Estadísticas de Cp:")
    print(stats)