from modulos.archivo import guardar_en_csv
from modulos.validaciones import entrada_numerica
from colorama import Fore
import emoji

def datos_biomedicos(usuario, datos):
    """Registra un nuevo estudiante con 8 campos, incluyendo placeholders para presión."""
    print(Fore.CYAN + "\n--- REGISTRO DE ESTUDIANTE ---")
    id_estudiante = entrada_numerica("Ingrese el ID del estudiante: ", int)
    nombre = input(Fore.YELLOW + "Nombre completo: ").strip()
    edad = entrada_numerica("Edad: ", int)
    peso = entrada_numerica("Peso (kg): ", float)
    estatura = entrada_numerica("Estatura (m): ", float)
    imc = round(peso / (estatura ** 2), 2)
    
    nuevo_estudiante = [
        id_estudiante, nombre, edad, peso, estatura, imc, None, None
    ]
    datos.append(nuevo_estudiante)
    
    if guardar_en_csv(datos, usuario):
        print(Fore.GREEN + emoji.emojize("\U0001F4AA ¡Estudiante registrado!"))
    else:
        print(Fore.RED + "Error al guardar. Intente nuevamente.")