from PIL import Image, ImageDraw
import os
import time

def aplicar_franja_base(ruta_imagen_original, ruta_imagen_salida, altura_franja_porcentaje, 
                       posicion_x_franja_porcentaje, posicion_y_franja_porcentaje):
    """Abre la imagen, dibuja la franja negra base y la guarda. Sin texto ni fuente."""
    try:
        # 1. Abrir la imagen
        img = Image.open(ruta_imagen_original).convert("RGB")
        ancho, alto = img.size

        # 2. Definir dimensiones de la franja
        altura_franja_pixeles = int(alto * altura_franja_porcentaje)
        
        # 3. Calcular la posición inicial y final de la franja
        x_franja_inicio = int(ancho * posicion_x_franja_porcentaje)
        y_franja_inicio = int(alto * posicion_y_franja_porcentaje)
        
        # La franja siempre va de borde a borde horizontalmente
        x_franja_fin = ancho
        y_franja_fin = y_franja_inicio + altura_franja_pixeles

        # Asegurar límites
        x_franja_inicio = max(0, x_franja_inicio)
        y_franja_inicio = max(0, y_franja_inicio)
        x_franja_fin = min(ancho, x_franja_fin) 
        y_franja_fin = min(alto, y_franja_fin)

        # 4. Dibujar la franja negra
        draw = ImageDraw.Draw(img)
        draw.rectangle([x_franja_inicio, y_franja_inicio, x_franja_fin, y_franja_fin], fill="black")

        # 5. Guardar la imagen modificada
        img.save(ruta_imagen_salida)
        print(f"✅ BASE CREADA: {os.path.basename(ruta_imagen_original)} -> Guardada en '{os.path.basename(ruta_imagen_salida)}'")

    except Exception as e:
        print(f"❌ Error al procesar '{ruta_imagen_original}': {e}")


# --- CONFIGURACIÓN PRINCIPAL (Diseño de la Franja) ---

# 1. Directorios
# Carpeta con tus imágenes ORIGINALES
carpeta_entrada = "C:\\Users\\Franco\\Desktop\\inquebrantable\\editar" 
# Carpeta TEMPORAL para las bases con franja, listas para recibir texto.
carpeta_temporal = os.path.join(carpeta_entrada, "temporal_bases") 

# 2. Parámetros Globales para el diseño
ALTURA_FRANJA = 0.04 # 4% del alto de la imagen
POSICION_X_FRANJA_PORCENTAJE = 0.0  # Inicia en el borde izquierdo
POSICION_Y_FRANJA_PORCENTAJE = 0.8  # 80% del alto (cerca del fondo)
# --------------------------------------------------

# --- LÓGICA DE PROCESAMIENTO POR LOTES ---

# 1. Crear la carpeta temporal si no existe
if not os.path.exists(carpeta_temporal):
    os.makedirs(carpeta_temporal)
    print(f"Creando carpeta temporal: {carpeta_temporal}")

# 2. Verificar que la carpeta de entrada exista
if not os.path.exists(carpeta_entrada):
    print(f"❌ Error: La carpeta de entrada '{carpeta_entrada}' no existe.")
    exit()

print(f"\nIniciando preparación de {ALTURA_FRANJA*100}% franjas base...")

imagenes_procesadas = 0
for nombre_archivo in os.listdir(carpeta_entrada):
    # Ignoramos la carpeta de salida y solo procesamos imágenes
    if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and nombre_archivo != os.path.basename(carpeta_temporal):
        
        ruta_original = os.path.join(carpeta_entrada, nombre_archivo)
        
        # Guardar la imagen con la franja en la carpeta TEMPORAL
        # Mantenemos el nombre original para que el script 2 pueda relacionarlas
        ruta_salida = os.path.join(carpeta_temporal, nombre_archivo) 

        aplicar_franja_base(ruta_original, ruta_salida, ALTURA_FRANJA, 
                            POSICION_X_FRANJA_PORCENTAJE, POSICION_Y_FRANJA_PORCENTAJE)
        imagenes_procesadas += 1

if imagenes_procesadas == 0:
    print(f"⚠️ No se encontraron imágenes soportadas en la carpeta '{carpeta_entrada}'.")

print("\n✨ Proceso de preparación de bases completado. Las bases están en la carpeta 'temporal_bases'.")
print("El siguiente paso es ejecutar el script de contenido (Script 2).")