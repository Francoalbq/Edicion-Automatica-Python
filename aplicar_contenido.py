from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd
import numpy as np 

# --- CONFIGURACIÓN PRINCIPAL ---

# 1. Directorios y Archivos
# La carpeta de entrada es la carpeta TEMPORAL que generó el Script 1
carpeta_temporal = "C:\\Users\\Franco\\Desktop\\inquebrantable\\editar\\temporal_bases" 
# La carpeta de salida final para las imágenes terminadas
carpeta_salida = "C:\\Users\\Franco\\Desktop\\inquebrantable\\editar\\imagenes_editadas" 

# RUTA AJUSTADA para frases.csv
ARCHIVO_DE_TEXTOS = os.path.join(carpeta_temporal, "frases.csv") 

# 2. Parámetros Globales (¡Deben ser los mismos que en el Script 1!)
ALTURA_FRANJA = 0.04 
POSICION_X_FRANJA_PORCENTAJE = 0.0 
POSICION_Y_FRANJA_PORCENTAJE = 0.8  

# 3. Parámetros del Texto
RUTA_DE_LA_FUENTE = "C:\\Users\\Franco\\Desktop\\inquebrantable\\Archivo-VariableFont_wdth,wght.ttf" 
# Parámetros de Sombra
OFFSET_SOMBRA = 0
COLOR_SOMBRA = "gray" 
COLOR_TEXTO = "white"
# -------------------------------

def aplicar_contenido(ruta_imagen, texto_franja, ruta_fuente, info_franja):
    """Aplica texto, fuente y sombra a la imagen base con franja."""
    try:
        img = Image.open(ruta_imagen)
        ancho, alto = img.size
        draw = ImageDraw.Draw(img)

        # 1. Recalcular las dimensiones de la franja (igual que en el Script 1)
        altura_franja_pixeles = int(alto * info_franja['altura'])
        x_franja_inicio = int(ancho * info_franja['x_pos'])
        y_franja_inicio = int(alto * info_franja['y_pos'])
        x_franja_fin = ancho 

        # 2. Configurar Fuente y Tamaño
        tamanio_base_fuente = int(altura_franja_pixeles * 0.4) 
        if tamanio_base_fuente == 0:
            tamanio_base_fuente = 1 
        fuente = ImageFont.truetype(ruta_fuente, tamanio_base_fuente)

        # 3. Obtener dimensiones del texto para centrarlo
        caja_texto = draw.textbbox((0, 0), texto_franja, font=fuente)
        ancho_texto = caja_texto[2] - caja_texto[0]
        alto_texto = caja_texto[3] - caja_texto[1]

        # 4. Calcular la posición centrada dentro de la franja
        posicion_x_principal = x_franja_inicio + (x_franja_fin - x_franja_inicio - ancho_texto) / 2
        posicion_y_principal = y_franja_inicio + (altura_franja_pixeles - alto_texto) / 2

        # 5. Dibujar la sombra
        draw.text((posicion_x_principal + OFFSET_SOMBRA, posicion_y_principal + OFFSET_SOMBRA), 
                  texto_franja, font=fuente, fill=COLOR_SOMBRA)

        # 6. Dibujar el texto principal
        draw.text((posicion_x_principal, posicion_y_principal), 
                  texto_franja, font=fuente, fill=COLOR_TEXTO)

        return img

    except Exception as e:
        print(f"❌ Error al aplicar contenido a {os.path.basename(ruta_imagen)}: {e}")
        return None


# --- LÓGICA DE PROCESAMIENTO POR LOTES FINAL ---

# Verificar existencia de directorios y archivos clave
if not os.path.exists(carpeta_temporal):
    print(f"❌ ERROR: La carpeta de bases temporales '{carpeta_temporal}' no existe. Ejecuta el Script 1 primero.")
    exit()
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)
if not os.path.exists(RUTA_DE_LA_FUENTE):
    print(f"❌ ERROR: El archivo de fuente '{RUTA_DE_LA_FUENTE}' no se encontró.")
    exit()

# 1. Cargar datos de Excel/CSV
try:
    # ¡CORRECCIÓN CLAVE!: Forzar el uso del punto y coma como delimitador
    df = pd.read_csv(ARCHIVO_DE_TEXTOS, encoding='utf-8', sep=';')
    df = df.replace({np.nan: ''}) 
    df['nombre_archivo'] = df['nombre_archivo'].str.lower()
    print(f"Datos de texto cargados desde '{os.path.basename(ARCHIVO_DE_TEXTOS)}'. Total de {len(df)} filas.")
except FileNotFoundError:
    print(f"❌ ERROR: No se encontró el archivo de textos en la ruta esperada: '{ARCHIVO_DE_TEXTOS}'.")
    exit()
except KeyError as e:
    print(f"❌ ERROR DE COLUMNA: No se encontró la columna esperada: {e}")
    print("Por favor, verifica que tu CSV tenga las columnas 'nombre_archivo' y 'texto_franja' escritas exactamente así.")
    exit()


# ----------------------------------------------------
# SECCIÓN DE DEPURACIÓN (DEBUG)
# ----------------------------------------------------
print("\n--- DEBUG: Nombres de Archivo ---")

# Nombres en el CSV
nombres_csv = df['nombre_archivo'].unique().tolist()
# Limpiamos los nombres del CSV de cualquier espacio extra o comillas que pueda haber quedado
nombres_csv = [n.strip().replace('"', '').replace("'", "") for n in nombres_csv]
print(f"Nombres ÚNICOS encontrados en {os.path.basename(ARCHIVO_DE_TEXTOS)} (CSV):\n{nombres_csv}")

# Nombres en la carpeta
nombres_carpeta = [f.lower() for f in os.listdir(carpeta_temporal) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
print(f"\nNombres encontrados en la carpeta '{os.path.basename(carpeta_temporal)}':\n{nombres_carpeta}")

# Mostrar los nombres que faltan en el CSV
archivos_faltantes_en_csv = [f for f in nombres_carpeta if f not in nombres_csv]
if archivos_faltantes_en_csv:
    print(f"\n❌ ARCHIVOS SIN COINCIDENCIA EN CSV (Arregla los nombres en el CSV):\n{archivos_faltantes_en_csv}")
else:
    print("\n✅ Todos los archivos de la carpeta tienen un nombre en el CSV. ¡Debería funcionar!")

print("------------------------------------\n")
# ----------------------------------------------------

info_franja = {
    'altura': ALTURA_FRANJA,
    'x_pos': POSICION_X_FRANJA_PORCENTAJE,
    'y_pos': POSICION_Y_FRANJA_PORCENTAJE
}

# 2. Iterar sobre las bases y aplicar el contenido
imagenes_finalizadas = 0
for nombre_archivo in os.listdir(carpeta_temporal):
    nombre_archivo_lower = nombre_archivo.lower()
    
    # Solo procesamos imágenes
    if nombre_archivo_lower.endswith(('.png', '.jpg', '.jpeg', '.webp')):
    
        # 3. Buscar el texto correspondiente en el DataFrame
        # Limpiamos el nombre de la imagen antes de buscarla en el dataframe
        nombre_limpio = nombre_archivo_lower.strip().replace('"', '').replace("'", "")
        fila_texto = df[df['nombre_archivo'].str.strip().str.lower().replace('"', '').replace("'", "") == nombre_limpio]

        if not fila_texto.empty:
            texto_a_insertar = str(fila_texto['texto_franja'].iloc[0])

            if texto_a_insertar.strip() != '':
                ruta_imagen = os.path.join(carpeta_temporal, nombre_archivo)
                
                imagen_final = aplicar_contenido(ruta_imagen, texto_a_insertar, RUTA_DE_LA_FUENTE, info_franja)

                if imagen_final:
                    # 4. Guardar la imagen final
                    nombre_base, ext = os.path.splitext(nombre_archivo)
                    ruta_salida_final = os.path.join(carpeta_salida, f"{nombre_base}_FINAL.jpg")
                    imagen_final.save(ruta_salida_final)
                    print(f"✅ FINALIZADO: {nombre_archivo} -> Texto: '{texto_a_insertar}'")
                    imagenes_finalizadas += 1
            else:
                print(f"ℹ️ Advertencia: El archivo '{nombre_archivo}' tiene texto vacío en el CSV, omitido.")

print(f"\n✨ Proceso")