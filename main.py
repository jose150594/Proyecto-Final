from modulos.usuario import registrar_usuario, iniciar_sesion
from modulos.registro import datos_biomedicos
from modulos.analisis import clasificar_imc, altura_extremos, peso_extremos, analizar_presion_arterial
from modulos.graficos import graficar_datos
from modulos.busqueda import busqueda, mostrar_datos_dataframe
from modulos.archivo import cargar_desde_csv, guardar_en_csv
from modulos.reporte import generar_reporte_pdf
from modulos.presion import monitoreo_presion
from colorama import init, Fore
import emoji

init(autoreset=True)

def submenu_analisis(usuario):
    while True:
        print(Fore.CYAN + "\n--- Submenú de Análisis ---")
        print("1️⃣ Clasificar IMC")
        print("2️⃣ Mostrar extremos de altura")
        print("3️⃣ Mostrar extremos de peso")
        print("4️⃣ Analizar presión arterial")
        print("5️⃣ Volver al menú principal")
        
        opcion = input(Fore.YELLOW + "Opción: ").strip()
        if opcion == "1":
            clasificar_imc(usuario)
        elif opcion == "2":
            altura_extremos(usuario)
        elif opcion == "3":
            peso_extremos(usuario)
        elif opcion == "4":
            analizar_presion_arterial(usuario)
        elif opcion == "5":
            break
        else:
            print(Fore.RED + "Opción inválida.")

def main():
    print(Fore.CYAN + "--- BIENVENIDO AL SISTEMA ---")
    usuario_actual = None
    
    # Autenticación
    while not usuario_actual:
        opcion = input(Fore.YELLOW + "¿Ya tienes cuenta? (si/no): ").lower().strip()
        
        if opcion == 'si':
            usuario_input = input(Fore.YELLOW + "Usuario: ").strip()
            if iniciar_sesion(usuario_input):
                usuario_actual = usuario_input
            else:
                print(Fore.RED + "Credenciales incorrectas. Intente de nuevo.")
        
        elif opcion == 'no':
            usuario_actual = registrar_usuario()
        else:
            print(Fore.RED + "Opción no válida.")
    
    # Carga inicial de datos
    datos = cargar_desde_csv(usuario_actual)
    
    while True:
        print(Fore.CYAN + "\n--- MENÚ PRINCIPAL ---")
        print("1️⃣ Registrar datos biomédicos")
        print("2️⃣ Monitorear presión arterial")
        print("3️⃣ Guardar datos en CSV")
        print("4️⃣ Cargar y mostrar datos")
        print("5️⃣ Buscar estudiante")
        print("6️⃣ Análisis de datos")
        print("7️⃣ Graficar datos")
        print("8️⃣ Generar reporte PDF")
        print("9️⃣ Salir")
        
        opcion = input(Fore.YELLOW + "Opción: ").strip()
        
        if opcion == "1":
            datos_biomedicos(usuario_actual, datos)
            datos = cargar_desde_csv(usuario_actual)  # Recarga datos actualizados
            
        elif opcion == "2":
            id_estudiante = int(input(Fore.YELLOW + "ID del estudiante: "))
            monitoreo_presion(usuario_actual, id_estudiante)
            datos = cargar_desde_csv(usuario_actual)  # Recarga datos actualizados
            
        elif opcion == "3":
            if guardar_en_csv(datos, usuario_actual):
                print(Fore.GREEN + "¡Datos guardados correctamente!")
            datos = cargar_desde_csv(usuario_actual)  # Recarga datos
            
        elif opcion == "4":
            mostrar_datos_dataframe(usuario_actual)
            
        elif opcion == "5":
            id_estudiante = int(input(Fore.YELLOW + "ID del estudiante: "))
            busqueda(usuario_actual, id_estudiante)
            
        elif opcion == "6":
            submenu_analisis(usuario_actual)
            
        elif opcion == "7":
            graficar_datos(usuario_actual)
            
        elif opcion == "8":
            generar_reporte_pdf(usuario_actual)
            
        elif opcion == "9":
            print(Fore.MAGENTA + "¡Hasta pronto!")
            break
            
        else:
            print(Fore.RED + "Opción inválida.")

if __name__ == "__main__":
    main()