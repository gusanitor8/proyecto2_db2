def choose_mode():
    """
    Función que permite al usuario elegir el modo de la aplicación
    :return: integer
    """
    print("Elige un modo: ")
    print("0. Salir")
    print("1. Modo Usuario")
    print("2. Modo Administrador")

    try:
        mode = int(input("Ingrese el dígito respectivo: "))

        if mode > 2 or mode < 0:
            raise ValueError

    except ValueError:
        print("Por favor, ingrese un numero dentro del rango\n")
        return choose_mode()

    return mode


def get_dpi():
    """
    Función que permite al usuario ingresar su DPI
    :return: integer
    """

    dpi = str(input("Ingrese su DPI: "))

    return dpi
