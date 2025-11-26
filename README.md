# 🖼️ Edición Automática de Imágenes con Franja de Texto

Este proyecto en Python automatiza la tarea de agregar una **franja negra** y un **texto personalizado** a múltiples imágenes en un flujo de dos etapas, utilizando un archivo de datos (CSV) como guía.

## ⚙️ Flujo de Trabajo (Dos Etapas)

La automatización se realiza mediante dos scripts que deben ejecutarse **en orden**.

| Script | Propósito Principal | Salida Generada |
| :--- | :--- | :--- |
| **`automation.py`** | **PREPARACIÓN DE BASES** Crea una copia temporal de todas las imágenes originales y les dibuja la franja negra base, sin texto. | Directorio: `editar/temporal_bases` |
| **`aplicar_contenido.py`** | **APLICACIÓN DE CONTENIDO** Lee el archivo CSV, asocia el texto a la imagen correcta y lo superpone con la fuente y color definidos. | Directorio: `editar/imagenes_editadas` |

---

## 💾 Integración con Excel/CSV

La clave del contenido personalizado es el archivo **`frases.csv`**.

1.  **Formato:** Debes crear o exportar una hoja de cálculo desde **Excel** (o Google Sheets) como un archivo **CSV**.
2.  **Delimitador:** El script `aplicar_contenido.py` está configurado para leer el archivo usando el **punto y coma (`;`)** como delimitador, común en muchas configuraciones regionales.
3.  **Columnas Requeridas:**
    * `nombre_archivo`: El nombre **exacto** del archivo de imagen (ej: `imagen_001.jpg`).
    * `texto_franja`: El texto que se insertará en la franja de esa imagen.

---

## 📚 Librerías de Python Requeridas

Este proyecto necesita las siguientes librerías, las cuales deben ser instaladas en tu entorno virtual:

```bash
pip install Pillow pandas numpy
