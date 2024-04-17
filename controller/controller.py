from view.menus import *

global_dpi = ""

def run():
    while True:
        opcion_principal = menu_principal()

        # Administrador
        if opcion_principal == "1":
            opcion_administrador = modo_administrador()

            if opcion_administrador == "1":
                print("\nHas seleccionado desactivar cuenta de usuario o empresa.")
                desactivar_cuenta()

            elif opcion_administrador == "2":
                clasificar_cuentas_fraudulentas()

            elif opcion_administrador == "3":
                marcar_cuenta_fraudulenta()

            elif opcion_administrador == "4":
                marcar_cuentas_fraudulentas()

            elif opcion_administrador == "5":
                borrar_propiedad_fraude()

            elif opcion_administrador == "6":
                print("Regresando al menú principal...")
                print("")
                menu_principal()  # Regresar al menú principal

        # Cliente
        elif opcion_principal == "2":
            global_dpi = input("Ingrese su DPI: ")

            opcion_cliente = modo_cliente()

            if opcion_cliente == "1":
                crear_usuario_individuo(global_dpi)

            elif opcion_cliente == "2":
                crear_usuario_empresa()

            elif opcion_cliente == "3":
                crear_cuenta(global_dpi)

            elif opcion_cliente == "4":
                agregar_celular_correo(global_dpi)

            elif opcion_cliente == "5":
                hacer_transferencia(global_dpi)

            elif opcion_cliente == "6":
                eliminar_propiedades(global_dpi)

            elif opcion_cliente == "7":
                actualizar_celular_correo(global_dpi)

            elif opcion_cliente == "8":
                actualizar_titulacion(global_dpi)

            elif opcion_cliente == "9":
                eliminar_usuario(global_dpi)

            elif opcion_cliente == "10":
                informacion_usuario(global_dpi)

            elif opcion_cliente == "11":
                ver_cuentas(global_dpi)

            elif opcion_cliente == "12":
                informacion_cuenta(global_dpi)

            elif opcion_cliente == "13":
                print("Regresando al menú principal...")
                print("")
                menu_principal(global_dpi)

        # Salir
        elif opcion_principal == "3":
            print("Gracias por utilizar nuestros servicios. ¡Hasta luego!")
            print("")
            exit()


