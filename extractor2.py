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
            pagina = pdf.pages+[0] #Trabajamos con la primera pagina
            
            # Recorremos cada campo definido en tu plantilla
            for campo, coords in plantilla_factura.items():
                valor = extraer_campo(pagina, campo, coords)
                datos_factura[campo] = valor
                print(f"  > {campo}: {valor}")
                
        return datos_factura
    
    except Exception as e:
        print(f"Error abriendo el PDF: {e}")
        return None
    
# --- 3. BLOQUE PRINCIPAL (MAIN) ---
if __name__ == "__main__":
    
    # A. Verificamos que el PDF exista
    if not os.path.exists(ARCHIVO_PDF):
        print(f"¡ERROR! No encuentro el archivo '{ARCHIVO_PDF}'")
    else:
        # B. Extraemos los datos
        resultados = procesar_documento()
        
        if resultados:
            print("\n--- Guardando en Excel ---")
            
            # C. Creamos el Excel usando Pandas
            # Pandas necesita una lista de diccionarios (una lista de filas)
            lista_filas = [resultados]
            
            df = pd.DataFrame(lista_filas)
            
            try:
                df.to_excel(ARCHIVO_EXCEL, index=False)
                print(f"¡Exito Total!")
                print(f"Los datos se guardaron en: {ARCHIVO_EXCEL}")
            except PermissionError:
                print("ERROR: No pude gardar el Excel. ¡Cierra el archivo si lo tienes abierto!")
            
            