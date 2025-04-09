from colorama import Fore
import emoji

def entrada_numerica(mensaje, tipo=float):
    while True:
        entrada = input(mensaje)
        try:
            valor = tipo(entrada)
            if valor <= 0:
                print(Fore.RED + emoji.emojize("\U000026A0  El valor debe ser positivo."))
            else:
                return valor
        except ValueError:
            print(Fore.RED + emoji.emojize("\U0000274C Entrada inválida. Ingrese un número válido."))
