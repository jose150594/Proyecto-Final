import csv
import os
from colorama import Fore
import emoji
import logging

logging.basicConfig(
    filename='archivo.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def guardar_en_csv(datos, usuario):
    """Guarda todos los datos en el CSV, incluyendo presiones."""
    nombre_archivo = f"estudiantes_{usuario}.csv"
    try:
        with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([
                "ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", 
                "IMC", "Presión Sistólica", "Presión Diastólica"
            ])
            escritor.writerows(datos)
        return True
    except Exception as e:
        logging.error(f"Error al guardar: {e}")
        return False

def cargar_desde_csv(usuario):
    """Carga los datos asegurando 8 columnas y tipos correctos."""
    nombre_archivo = f"estudiantes_{usuario}.csv"
    datos = []
    try:
        if not os.path.exists(nombre_archivo):
            return datos
            
        with open(nombre_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            next(lector)  # Saltar encabezado
            for fila in lector:
                if len(fila) != 8:
                    continue
                datos.append([
                    int(fila[0]),        # ID
                    fila[1],             # Nombre
                    int(fila[2]),        # Edad
                    float(fila[3]),      # Peso
                    float(fila[4]),      # Estatura
                    float(fila[5]),     # IMC
                    int(fila[6]) if fila[6] else None,  # Sistólica
                    int(fila[7]) if fila[7] else None   # Diastólica
                ])
        return datos
    except Exception as e:
        logging.error(f"Error al cargar: {e}")
        return []