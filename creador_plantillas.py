import tkinter as tk
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import sys

# Ajusta esto all nombre de tu pdf
PDF_A_PROCESAR = "FacturaSencilla.pdf"

class SeleccionadorVisual:
    def __init__(self, master, ruta_pdf):
        self.master = master
        self.master.title("Creador de Plantillas - Proyecto Max")
        
        # 1. Convertir la primara página del PDF a imagen para mostrarla
        # Usamos 72 dpi para qeu tenga un tamaño similar a la pantalla
        print("Cargaando PDF... ")
        imagenes = convert_from_path(ruta_pdf, dpi=72)
        self.imagen_original = imagenes[0]
        self.tk_imagen = ImageTk.PhotoImage(self.imagen_original)
        
        # 2 . Crear el canvas (el lienzo donde dibujamos)
        self.canvas = tk.Canvas(master, width=self.tk_imagen.width(), height=self.tk_imagen.height())
        self.canvas.pack()
        
        # Poner la imagen en el canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_imagen)
        
        # Variables para almacenar las coordenadas del mouse
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        
        # 3. Vincular los clics del mouse
        self.canvas.bind("<ButtonPress-1>", self.al_hacer_clic)
        self.canvas.bind("<B1-Motion>", self.al_arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self.al_soltar)
        
        print("--- INSTRUCCIONES ---")
        print("Dibuja un recuadro sobre el dato que quieres extraer.")
        print("Las coordenadas aparecerán aquí abajo.\n")
        
    def al_hacer_clic(self, event):
        # Guardamos donde empezó el clic
        self.start_x = event.x
        self.start_y = event.y
        # Si ya habia un rectángulo, lo borramos para dibujar uno nuevo
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            
    def al_arrastrar(self, event):
        # Mientras arrastra, actualizamos el dibujo del rectángulo rojo
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline="red", width=2
        )
    
    def al_soltar(self, event):
        # Al soltar, calculammos las coordenadas finales
        end_x, end_y = event.x, event.y
        
        # Ordenamos las coordenadas (por si dibujó de abajo a arriba)
        x0 = min(self.start_x, end_x)
        y0 = min(self.start_y, end_y)
        x1 = max(self.start_x, end_x)
        y1 = max(self.start_y, end_y)
        
        # Ajuste de escala:
        # Como pdfplumber a veces usa 72dpi por defecto y pdf2image también,
        # estas coordenadas suelen servir directamente
        
        print(f"Zona seleccionada: ({x0}, {y0}, {x1}, {y1})")
        print(f"--> Copia esto en tu extractor: coordenadas = ({x0}, {y0}, {x1}, {y1})")
        print("-" * 30)
        
if __name__ == "__main__":
    root = tk.Tk()
    # Verificación simple de archivo
    try:
        app = SeleccionadorVisual(root, PDF_A_PROCESAR)
        root.mainloop()
    except Exception as e:
        print(f"Error al abrir la interfaz: {e}")
        print("Asegurate de que el nombre del PDF en el código sea correcto.")
        