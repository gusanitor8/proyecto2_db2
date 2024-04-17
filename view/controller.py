from menus import menu_principal, menu_administrador, menu_cliente

def run():
    while True:
        opcion_principal = menu_principal()

        if opcion_principal == "1":
            opcion_administrador = menu_administrador()
            menu_administrador(opcion_administrador)
            
        elif opcion_principal == "2":
            opcion_cliente = menu_cliente()
            menu_cliente(opcion_cliente)
            
        elif opcion_principal == "3":
            print("Gracias por utilizar nuestros servicios. ¡Hasta luego!")
            break

run()