from view.menus import menu_principal


def run_():
    option = menu_principal()

    if option == "1":
        modo_administrador()
        # llamadas al backend

    elif option == "2":
        modo_cliente()


def modo_administrador():
    pass

def modo_cliente():
    pass
