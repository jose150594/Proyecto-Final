import os
from colorama import Fore
import emoji
import logging

# Configuración de logging
logging.basicConfig(
    filename='usuario.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def registrar_usuario():
    while True:
        print(Fore.CYAN + "\n--- REGISTRO DE USUARIO ---")
        usuario = input(Fore.YELLOW + "Ingrese un nombre de usuario: ").strip()
        
        # Validar usuario no vacío
        while not usuario:
            print(Fore.RED + "¡El usuario no puede estar vacío!")
            usuario = input(Fore.YELLOW + "Ingrese un nombre de usuario: ").strip()
        
        # Validar contraseña
        while True:
            password = input(Fore.YELLOW + "Ingrese una contraseña: ").strip()
            if not password:
                print(Fore.RED + "¡La contraseña no puede estar vacía!")
                continue
            password_confirm = input(Fore.YELLOW + "Confirme su contraseña: ").strip()
            if password == password_confirm:
                break
            print(Fore.RED + emoji.emojize("\U0000274C Las contraseñas no coinciden. Intente de nuevo."))

        # Guardar usuario
        try:
            mode = 'a' if os.path.exists('usuarios.txt') else 'w'
            with open('usuarios.txt', mode, encoding='utf-8') as archivo:
                if mode == 'a':
                    # Verificar si el usuario ya existe
                    with open('usuarios.txt', 'r', encoding='utf-8') as f:
                        usuarios = [line.split(":")[0].strip() for line in f.readlines()]
                        if usuario in usuarios:
                            print(Fore.RED + emoji.emojize("\U000026A0 Usuario ya existe. Elija otro."))
                            continue
                archivo.write(f"{usuario}:{password}\n")
                print(Fore.GREEN + emoji.emojize("\U0001F4AA Registro exitoso!"))
                return usuario  # Retorna el usuario registrado
                
        except IOError as e:
            logging.error(f"Error al escribir en usuarios.txt: {e}")
            print(Fore.RED + emoji.emojize("\U0000274C Error al guardar el usuario."))
            return None

def iniciar_sesion(usuario_input):  # <- Ahora recibe el usuario como parámetro
    print(Fore.CYAN + "\n--- INICIO DE SESIÓN ---")
    password = input(Fore.YELLOW + "Ingrese su contraseña: ").strip()
    
    if not os.path.exists('usuarios.txt'):
        print(Fore.RED + emoji.emojize("\U000026A0 No hay usuarios registrados."))
        return False
    
    try:
        with open('usuarios.txt', 'r', encoding='utf-8') as archivo:
            for line in archivo.readlines():
                if not line.strip():
                    continue
                try:
                    stored_user, stored_pass = line.strip().split(":")
                    if stored_user == usuario_input and stored_pass == password:
                        print(Fore.GREEN + emoji.emojize("\U0001F44D ¡Sesión iniciada!"))
                        return True
                except ValueError:
                    logging.error(f"Línea corrupta: {line.strip()}")
        print(Fore.RED + emoji.emojize("\U0000274C Contraseña incorrecta."))
        return False
    except IOError as e:
        logging.error(f"Error al leer usuarios.txt: {e}")
        print(Fore.RED + emoji.emojize("\U0000274C Error al acceder al archivo."))
        return False