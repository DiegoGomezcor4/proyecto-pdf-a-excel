import pdfplumber
import pandas as pd
import os

# --- 1. CONFIGURACIÓN ---
CARPETA_PDFS = "pdfs_entrantes"  # La carpeta donde pusiste los archivos
ARCHIVO_EXCEL = "Reporte_Mensual.xlsx"

# --- 2. LA PLANTILLA (¡PON TUS NÚMEROS AQUÍ!) ---
plantilla_factura = {
    # Copia aquí las coordenadas que obtuviste con tu herramienta visual
    "Fecha":        (20, 205, 95, 221),  
    "NIF_Cliente":  (340, 174, 391, 186),
    "Cliente":      (302, 160, 447, 175),
    "Total":        (529, 708, 580, 721),
    "Num_Factura":  (128, 205, 167, 221)
}
 
def extraer_campo(pagina, nombre_campo, coordenadas):
    """Extrae datos de una zona, si las coordenadas son válidas"""
    if coordenadas == (0, 0, 0, 0):
        return ""
    try:
        area = pagina.crop(coordenadas)
        texto = area.extract_text()
        return texto.strip() if texto else ""
    except Exception:
        return ""

def procesar_un_pdf(ruta_completa):
    """Abre un PDF y aplica la plantilla"""
    datos = {}
    try:
        with pdfplumber.open(ruta_completa) as pdf:
            pagina = pdf.pages[0]
            for campo, coords in plantilla_factura.items():
                datos[campo] = extraer_campo(pagina, campo, coords)
        return datos
    except Exception as e:
        print(f"   [Error leyendo archivo]: {e}")
        return None

# --- 3. PROCESAMIENTO POR LOTES ---
if __name__ == "__main__":
    
    print(f"--- BUSCANDO ARCHIVOS EN '{CARPETA_PDFS}' ---")
    
    # Lista para acumular TODOS los datos de todas las facturas
    lista_maestra = []
    
    # 1. Verificar si la carpeta existe
    if not os.path.exists(CARPETA_PDFS):
        print(f"ERROR: Crea una carpeta llamada '{CARPETA_PDFS}' y pon los PDFs ahí.")
    else:
        # 2. Obtener lista de archivos
        archivos = os.listdir(CARPETA_PDFS)
        
        # Filtramos para que solo lea PDFs (por si hay otras cosas)
        pdfs = [a for a in archivos if a.lower().endswith(".pdf")]
        
        print(f"Se encontraron {len(pdfs)} documentos para procesar.\n")
        
        # 3. Bucle: Procesar uno por uno
        for archivo in pdfs:
            print(f"Procesando: {archivo} ...")
            
            # Construimos la ruta completa (ej: pdfs_entrantes/factura_enero.pdf)
            ruta = os.path.join(CARPETA_PDFS, archivo)
            
            # Extraemos
            datos = procesar_un_pdf(ruta)
            
            if datos:
                # Añadimos el nombre del archivo para saber de cuál vino
                datos["Nombre_Archivo"] = archivo 
                
                # Guardamos en la lista maestra
                lista_maestra.append(datos)

        # 4. Generar Excel Final
        if lista_maestra:
            print("\n--- GENERANDO EXCEL ---")
            df = pd.DataFrame(lista_maestra)
            
            # Reordenar columnas para que 'Nombre_Archivo' salga primero (estética)
            columnas = ["Nombre_Archivo"] + [k for k in plantilla_factura.keys()]
            df = df[columnas]
            
            df.to_excel(ARCHIVO_EXCEL, index=False)
            print(f"¡TERMINADO! Se procesaron {len(lista_maestra)} facturas.")
            print(f"Abre el archivo: {ARCHIVO_EXCEL}")
        else:
            print("No se extrajeron datos. Revisa las coordenadas o la carpeta.")