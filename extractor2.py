import pdfplumber
import pandas as pd # Pare crear el Excel
import os

# --- 1. Configuración inicial ---
ARCHIVO_PDF = "FacturaSencilla.pdf" # Nombre exacto del tu archivo
ARCHIVO_EXCEL = "Resultado_Facturas.xlsx" # Nombre del Excel que se creará

# --- 2. TU PLANTILLA (Aquí es donde ocurrirá la magia) ---
# Usa 'creador_plantillas.py' para obtener estos números.
# Formato: (Izquierda, Arriba, Derecha, Abajo)

plantilla_factura = {
    # EJEMPLO:  "Fecha": (345, 550, 480, 570),
    # --- Pega tus numeros aqui abajo ---
    "Fecha": (345, 550, 480, 570),
    "Niv_Cliente": (0, 0, 0, 0),
    "Cliente": (0, 0, 0, 0),
    "Total": (0, 0, 0, 0),
    "Num_Factura": (0, 0, 0, 0),
}

def extraer_campo(pagina, nombre_campo, coordenadas):
    """
    Recorta una zona específica de la página y extrae texto.
    """
    # Si las coordenadas son 0, 0, 0, 0 ignoramos el campo
    if coordenadas == (0, 0, 0, 0):
        return "Pendiente de configurar"
    
    try:
        # Recortamos la zona (crop)
        area_recorte = pagina.crop(coordenadas)
        # Extraemos el texto
        texto = area_recorte.extract_text()
        
        # Limpiamos el texto (quitamos espacios extra al inicio y final)
        if texto:
            return texto.strip()
        else:
            return "[Vacio]"
        
    except Exception as e:
        return f"Error: {e}"
    
def procesar_documento():
    print(f"--- Iniciando extracción de: {ARCHIVO_PDF} ---")
    
    # Diccionario para guardar los datos de ESTA factura
    datos_factura = {}
    
    try:
        with pdfplumber.open(ARCHIVO_PDF) as pdf:
            
            