import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

def extraer_datos(ruta_pdf, coordenadas):
    """
    ruta_pdf: Ruta al archivo PDF:
    coordenadas: Tupla (x0, y0, x1, y1).
    """
    print(f"--- Procesandoo {ruta_pdf} ---")

    datos_extraidos = ""
    
    # 1. Intento Digital (pdfplumber)
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            pagina = pdf.pages[0]
            # pdfplumber recorta: (x0, top, x1, bottom)
            area_recorte = pagina.crop(coordenadas)
            texto = area_recorte.extract_text()
            
            if texto:
                return f"[Digital]: {texto.strip()}"
            
    except Exception as e:
        print(f"Nota: No se pudo leer digitalmente ({e})")
        
    # 2. Intento OCR (pytesseract)
    print("Texto digital no detectado o vacio. Aplicando OCR...")
    try:
        # Convertir PDF a imagen
        imagenes = convert_from_path(ruta_pdf, first_page=1, last_page=1)
        imagen_pag = imagenes[0] # Primera página
        
        # Recortar la imagen (La imagen usa el mismo sistema de coords que el PDF generalmente)
        imagen_recortada = imagen_pag.crop(coordenadas)
        
        #OCR
        texto_ocr = pytesseract.image_to_string(imagen_recortada)
        return f"[OCR]: {texto_ocr.strip()}"
    except Exception as e:
        return f"Error Falta: {e}"
    
# --- Zona de pruebas ---

if __name__ == "__main__":
    # 1 . Asegurate de tener un archivo llamado "factura.pdf" en la misma carpeta
    # o cambia el nombre aqui abajo:
    mi_pdf = "FacturaSencilla.pdf"
    
    # Si no tienen un PDF ahi, el script fallará, Creamos una verificación simple:
    if not os.path.exists(mi_pdf):
        print(f"Error! No se encontro el archivo '{mi_pdf}' en esta carpeta")
        print("Por favor, copia un PDF aquí para probar")
    else:
        # Coordenadas de prueba (x0, y0, x1, y1)
        #Prueba con un área grande para asegurar que agarre algo
        zona_prueba = (22, 205, 90, 221)
        
        resultado = extraer_datos(mi_pdf, zona_prueba)
        print("\n Resultado Final:")
        print(resultado)