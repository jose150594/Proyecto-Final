from modulos.archivo import cargar_desde_csv, guardar_en_csv
from colorama import Fore
import emoji

def monitoreo_presion(usuario, id_estudiante):
    datos = cargar_desde_csv(usuario)
    if not datos:
        print(Fore.RED + "No hay estudiantes registrados.")
        return

    for estudiante in datos:
        if estudiante[0] == id_estudiante:
            print(Fore.CYAN + f"\n--- ACTUALIZAR PRESIONES (ID: {id_estudiante}) ---")
            print(Fore.YELLOW + f"Valores actuales: Sistólica: {estudiante[6]}, Diastólica: {estudiante[7]}")
            
            # Solicita nuevas presiones
            try:
                estudiante[6] = int(input("Nueva presión sistólica: "))
                estudiante[7] = int(input("Nueva presión diastólica: "))
                
                if guardar_en_csv(datos, usuario):
                    print(Fore.GREEN + "¡Presiones actualizadas!")
                else:
                    print(Fore.RED + "Error al guardar.")
            except ValueError:
                print(Fore.RED + "¡Debe ingresar números enteros!")
            return
    
    print(Fore.YELLOW + "ID no encontrado.")