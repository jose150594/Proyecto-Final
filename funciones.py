# funciones.py
def entrada_numerica(mensaje, tipo=float):
    while True:
        entrada = input(mensaje)
        try:
            valor = tipo(entrada)
            if valor <= 0:
                print("El valor debe ser positivo.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número válido.")
