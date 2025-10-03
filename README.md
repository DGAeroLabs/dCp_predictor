# dCp_predictor
This program analyzes wing section dCp distributions, stores configurations and results to build a database, and generates normalized images for neural network training. It can recreate text data from images and verify image accuracy.

Primero se debe generar la poblacion a analizar mediante el modulo parametros.py
Luego al ejecutar el modulo CPWING.py se generara la base de datos compuesat de archivos txt que muestran la distribucion de dCp y imagenes normalizadas de las mismas
  El flujo de este calculo es:
    1. Se realizan los calculos aerodinamicos en OPENVSP y guarda archivos .slc con el valor de dCp de cada seccion y coordenada.
    2. Se reorganizan los valores de dCp en un formato X Y dCp sin encabezados y con solo numeros usando el modulo organizador.py
    3. Se calcula el minimo y el maximo dCp global con minimo.py
    4. Con test1 se generan imagenes normalizadas en blanco y negro donde blanco corresponde al dCp max y negro al dCp min

Para validar se hace lo siguiente
  1. usando img_to_txt.py se obtiene a partir de la imagen analizada un txt con las coordenas X y Y de 0 a 1 y el dCp correspondiente
  2. denormalizer.py transforma las coordenadas normales a reales tomando en cuenta el angulo de flechado y encogimiento del ala
  3. Para una representacion visual se puede usar comparador.py
