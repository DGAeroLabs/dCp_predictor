# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 19:08:42 2025

@author: Damian
"""

import openvsp as vsp
import numpy as np
import os
import time
import Organizador as org
import test1 as t1
import minimo as min


inicio = time.perf_counter()

print("Beginning CP analysis with parametric wing")

# Cargar las configuraciones desde el archivo .npy
try:
    configurations = np.load('wing_configurations.npy')
    print(f"✅ Loaded {len(configurations)} configurations from wing_configurations.npy")
    print("Column order: [Wing Area, Aspect Ratio, Taper Ratio, Sweep Angle, Flight Speed, Air Density]")
except FileNotFoundError:
    print("❌ Error: wing_configurations.npy not found. Please generate it first.")
    print("Run the configuration generator script before this one.")
    exit(1)



def process_configuration(config_idx, config):
    """
    Process a single configuration and save results
    """
    # Extraer parámetros de la configuración actual
    wing_area = config[0]
    aspect_ratio = config[1]
    taper_ratio = config[2]
    sweep_angle = config[3]
    flight_speed = config[6]
    air_density = config[7]
    
    print(f"\n{'='*50}")
    print(f"Processing configuration #{config_idx}")
    print(f"{'='*50}")
    print(f"Wing Area: {wing_area:.2f} m² | AR: {aspect_ratio:.2f} | Taper: {taper_ratio:.2f}")
    print(f"Sweep: {sweep_angle:.2f}° | Speed: {flight_speed:.2f} m/s | Density: {air_density:.3f} kg/m³")
    
    # ====== Derived Calculations ======
    span = (aspect_ratio * wing_area)**0.5  # Wingspan [m]
    tip_chord = 2 * wing_area / (span * (1 + taper_ratio))  # Root chord [m]
    root_chord = tip_chord * taper_ratio    # Tip chord [m]
    
    # ====== Panel Resolution Control ======
    chordwise_panels = 20   # Number of panels along chord (NSlices)
    spanwise_panels = 15    # Number of panels along span (NCircSlices)

    print("\n--> Generating Wing Geometry")
    print(f"Span: {span:.2f} m | Root Chord: {root_chord:.2f} m | Tip Chord: {tip_chord:.2f} m")
    print(f"Panel Resolution: {chordwise_panels} chordwise, {spanwise_panels} spanwise")

    # ====== Create Geometry ======
    vsp.ClearVSPModel()  # Ensure clean slate
    wing_id = vsp.AddGeom("WING")

    # FIRST Set fundamental parameters before updating
    vsp.SetParmVal(wing_id, "XSec_Num", "XSec_1", 2)  # Only root and tip sections
    vsp.SetParmVal(wing_id, "TotalArea", "WingGeom", float(wing_area))
    vsp.SetParmVal(wing_id, "Aspect", "XSec_1", float(aspect_ratio/2))
    vsp.SetParmVal(wing_id, "Taper", "XSec_1", float(taper_ratio)**-1)
    vsp.SetParmVal(wing_id, "Sweep", "XSec_1", float(sweep_angle))
    vsp.SetParmVal(wing_id, "Sweep_Location", "XSec_1", float(0))  # 0.0 = LE sweep
    vsp.SetParmVal(wing_id, "X_Rel_Location", "XForm", 0.0)

    # Explicitly set root and tip chords
    vsp.SetParmVal(wing_id, "Root_Chord", "XSec_1", float(root_chord))
    vsp.SetParmVal(wing_id, "Tip_Chord", "XSec_2", float(tip_chord))
    vsp.SetParmVal(wing_id, "Span", "XSec_1", span/2)  # Half span for each side
    
    
    vsp.SetParmVal(wing_id, "ThickChord", "XSecCurve_0", float(0.12))
    vsp.SetParmVal(wing_id, "Camber", "XSecCurve_0", float(0.02))
    vsp.SetParmVal(wing_id, "CamberLoc", "XSecCurve_0", float(0.4))
    vsp.SetParmVal(wing_id, "ThickChord", "XSecCurve_1", float(0.12))
    vsp.SetParmVal(wing_id, "Camber", "XSecCurve_1", float(0.02))
    vsp.SetParmVal(wing_id, "CamberLoc", "XSecCurve_1", float(0.4))

    # Set panel resolution
    vsp.SetParmVal(wing_id, "SectTess_U", "XSec_1", spanwise_panels)
    vsp.SetParmVal(wing_id, "InCluster", "XSec_1", float(0.9))
    vsp.SetParmVal(wing_id, "OutCluster", "XSec_1", float(0.4))
    
    vsp.SetParmVal(wing_id, "NSlices", "XSec_1", chordwise_panels)
    

    vsp.Update()

    # ====== Verification ======
    actual_AR = vsp.GetParmVal(wing_id, "TotalAR", "WingGeom")
    actual_taper = vsp.GetParmVal(wing_id, "Taper", "WingGeom")
    actual_sweep = vsp.GetParmVal(wing_id, "Sweep", "WingGeom")

    print("\n--> Verification")
    print(f"Specified AR: {aspect_ratio:.2f} | Actual AR: {actual_AR:.2f}")
    print(f"Specified Taper: {taper_ratio:.2f} | Actual Taper: {actual_taper:.2f}")
    print(f"Specified Sweep: {sweep_angle:.2f} | Actual Sweep: {actual_sweep:.2f}")

    # ====== Save Model ======
    fname = f"drone_{config_idx}.vsp3"
    print(f"\n--> Saving Vehicle File: {fname}")
    vsp.WriteVSPFile(fname)
    print("COMPLETE")

    # ====== VSPAERO Analysis ======
    print("\n--> Computing Geometry")
    vsp.SetAnalysisInputDefaults("VSPAEROComputeGeometry")
    vsp.SetIntAnalysisInput("VSPAEROComputeGeometry", "AnalysisMethod", [vsp.VORTEX_LATTICE])
    vsp.ExecAnalysis("VSPAEROComputeGeometry")

    print("\n--> Computing VSPAERO Sweep")
    vsp.SetAnalysisInputDefaults("VSPAEROSweep")
    vsp.SetIntAnalysisInput("VSPAEROSweep", "AnalysisMethod", [vsp.VORTEX_LATTICE])
    vsp.SetDoubleAnalysisInput("VSPAEROSweep", "AlphaStart", [2.0], 0)
    vsp.SetDoubleAnalysisInput("VSPAEROSweep", "AlphaEnd", [2.0], 0)
    vsp.SetIntAnalysisInput("VSPAEROSweep", "AlphaNpts", [1])
    
    # Convert speed to Mach
    speed_of_sound = 343.0  # m/s at sea level
    mach_number = flight_speed / speed_of_sound
    vsp.SetDoubleAnalysisInput("VSPAEROSweep", "MachStart", [mach_number], 0)
    
    rid = vsp.ExecAnalysis("VSPAEROSweep") #aqui se crea el drone_0_DegenGeom.slc
    vsp.PrintResults(rid)

    print("\n--> Generating Cp Slices")
    vsp.SetAnalysisInputDefaults("CpSlicer")
    first_cut = span * 0.0
    last_cut = span * 0.5
    number_cut = 20  # Número total de cortes deseado
    
    # Calculamos el paso correcto
    step_cut = (last_cut - first_cut) / (number_cut - 1)
    ycuts = [first_cut + i * step_cut for i in range(number_cut)]
    
    # Configuramos los parámetros
    vsp.SetIntAnalysisInput("CpSlicer", "AnalysisMethod", [vsp.VORTEX_LATTICE])
    vsp.SetDoubleAnalysisInput("CpSlicer", "YSlicePosVec", ycuts)
    vsp.ExecAnalysis("CpSlicer") #aqui en el drone_0_DegenGeom.slc se aumentan todos los slices 
    
    # Renombrar el archivo .slc generado
    output_slicefile = f"drone_{config_idx}_DegenGeom.slc"
    if os.path.exists(output_slicefile):
        new_filename = f"{config_idx}.slc"
        os.rename(output_slicefile, new_filename)
        print(f"\n✅ Saved Cp slice results as: {new_filename}")
    else:
        print(f"\n❌ Error: {output_slicefile} not generated for configuration {config_idx}")
    
    # Limpiar resultados intermedios
    try:
        os.remove("VSPAERO_run.ada")
        os.remove("VSPAERO_run.fmt")
        os.remove("VSPAERO_run.key")
        os.remove("VSPAERO_run.res")
        os.remove("VSPAERO_run.vspgeom")
    except:
        pass
    
    print(f"\n{'='*50}")
    print(f"Configuration #{config_idx} completed successfully!")
    print(f"Results saved as: {config_idx}.slc")
    print(f"{'='*50}\n")
    
    # Pequeña pausa para evitar problemas de concurrencia
    time.sleep(1)

# Procesar todas las configuraciones
for idx, config in enumerate(configurations): #analisis en openvsp
    process_configuration(idx, config)

print("\n" + "="*50)
print(f"ALL {len(configurations)} CONFIGURATIONS PROCESSED SUCCESSFULLY!")
print("="*50)
print(f"Generated {len(configurations)} .slc files (0.slc to {len(configurations)-1}.slc)")
print("Each file contains Cp slice data for the corresponding configuration")
print("="*50)

for idx, config in enumerate(configurations): #formato de .txt
    input_filename = f"{idx}.slc"
    output_pivot = "tabla_pivot.csv"
    output_columns = f"{idx}.txt"
    org.process_cp_data(input_filename, output_pivot, output_columns)
print("\n" + "="*50)
print(f"ALL {len(configurations)} CONFIGURATIONS PROCESSED SUCCESSFULLY!")
print("="*50)
print(f"Generated {len(configurations)} .txt files (0.txt to {len(configurations)-1}.txt)")
print("Each file contains filtered Cp slice data for the corresponding configuration")
print("="*50)

configurations = np.load('wing_configurations.npy')

all_min = float('inf')                              #encontrar el minimo total
for idx, config in enumerate(configurations):
    input_filename = f"{idx}.txt"
    dcp_min = min.find_min_dcp(input_filename, all_min)
    if dcp_min < all_min:
        all_min=dcp_min
        print(f" new minimum in {input_filename}")
        
all_max = float('-inf')                            #encontrar el minimo total
for idx, config in enumerate(configurations):
    input_filename = f"{idx}.txt"
    dcp_max = min.find_max_dcp(input_filename, all_max)
    if dcp_max > all_max:
        all_max = dcp_max
        print(f" new maximum in {input_filename}")
    
for idx, config in enumerate(configurations): #crear imagenes
    input_filename = f"{idx}.txt"
    output_pic = f"{idx}.png"
    t1.normalizador(input_filename, output_pic, all_min, all_max)
print("\n" + "="*50)
print(f"ALL {len(configurations)} CONFIGURATIONS PROCESSED SUCCESSFULLY!")
print("="*50)
print(f"Generated {len(configurations)} .png files (0.txt to {len(configurations)-1}.png")
print("Each file contains normalized Cp data for the corresponding configuration")
print("="*50)

fin = time.perf_counter()
duracion = fin - inicio
print("\n" + "="*50)
print(f"Tiempo de ejecución: {duracion:.4f} segundos")
print("\n" + "="*50)