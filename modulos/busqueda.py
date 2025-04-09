import pandas as pd
from modulos.archivo import cargar_desde_csv
from colorama import Fore, Style
import emoji

def busqueda(usuario, numero_de_identificacion):
    """
    Busca un estudiante por ID y muestra sus datos formateados.
    
    Args:
        usuario (str): Nombre de usuario asociado a los datos
        numero_de_identificacion (int): ID del estudiante a buscar
    """
    try:
        datos = cargar_desde_csv(usuario)
        if not datos:
            print(Fore.YELLOW + emoji.emojize("\U0001F50D No hay estudiantes registrados."))
            return

        encontrado = False
        for estudiante in datos:
            if estudiante[0] == numero_de_identificacion:
                print(Fore.CYAN + "\n--- DATOS DEL ESTUDIANTE ---")
                print(Fore.YELLOW + f"ID: {estudiante[0]}")
                print(Fore.YELLOW + f"Nombre: {estudiante[1]}")
                print(Fore.YELLOW + f"Edad: {estudiante[2]} años")
                print(Fore.YELLOW + f"Peso: {estudiante[3]} kg")
                print(Fore.YELLOW + f"Estatura: {estudiante[4]} m")
                print(Fore.YELLOW + f"IMC: {estudiante[5]:.2f}")
                print(Fore.YELLOW + f"Presión: {estudiante[6]}/{estudiante[7]}")
                print(Style.RESET_ALL)
                encontrado = True
                break

        if not encontrado:
            print(Fore.RED + emoji.emojize(f"\U0000274C No se encontró el ID {numero_de_identificacion}"))

    except Exception as e:
        print(Fore.RED + f"Error en búsqueda: {str(e)}")

def mostrar_datos_dataframe(usuario):
    """
    Muestra todos los datos en un DataFrame pandas con formato mejorado.
    
    Args:
        usuario (str): Nombre de usuario asociado a los datos
    """
    try:
        datos = cargar_desde_csv(usuario)
        if not datos:
            print(Fore.YELLOW + emoji.emojize("\U0001F50D No hay datos para mostrar."))
            return

        columnas = [
            "ID", "Nombre", "Edad", 
            "Peso (kg)", "Estatura (m)", "IMC", 
            "PSistólica", "PDiastólica"
        ]
        
        df = pd.DataFrame(datos, columns=columnas)
        
        # Configuración visual del DataFrame
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.colheader_justify', 'center')
        
        print(Fore.CYAN + "\n--- REGISTRO COMPLETO DE ESTUDIANTES ---")
        print(Fore.YELLOW + df.to_string(index=False))
        print(Style.RESET_ALL)
        
    except Exception as e:
        print(Fore.RED + f"Error al mostrar datos: {str(e)}")