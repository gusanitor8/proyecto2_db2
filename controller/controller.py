from view.menus import *
from controller.controller_functions import deactivate_user_accounts, mark_account_as_fraud, \
    edit_fraud_for_user_accounts, rm_fraud_prop_from_user_titulations, edit_fraude_in_titulacion
from controller.db_crud import *

global_dpi = ""


def run():
    while True:
        opcion_principal = menu_principal()

        # Administrador
        if opcion_principal == "1":
            opcion_administrador = modo_administrador()

            if opcion_administrador == "1":
                print("\nHas seleccionado desactivar cuenta de usuario o empresa.")
                dpi, is_dpi = desactivar_cuenta()
                deactivate_user_accounts(dpi, is_dpi=is_dpi)


            elif opcion_administrador == "2":
                account_no: int = clasificar_cuentas_fraudulentas()
                mark_account_as_fraud(account_no)


            elif opcion_administrador == "3":
                no_cuenta, fraudulenta = marcar_cuenta_fraudulenta()
                mark_account_as_fraud(no_cuenta, fraudulenta)

            elif opcion_administrador == "4":
                dpi, fraude = marcar_cuentas_fraudulentas()
                edit_fraud_for_user_accounts(dpi, fraude)

            elif opcion_administrador == "5":
                dpi = borrar_propiedad_fraude()
                if type(dpi) is int:
                    rm_fraud_prop_from_user_titulations(dpi)

            elif opcion_administrador == "6":
                dpi, fraude = editar_fraude_en_titulaciones()
                edit_fraude_in_titulacion(dpi, fraude)


            elif opcion_administrador == "7":
                print("Regresando al menú principal...")
                print("")
                menu_principal()  # Regresar al menú principal

        # Cliente
        elif opcion_principal == "2":
            global_dpi = input("Ingrese su DPI: ")

            opcion_cliente = modo_cliente()

            if opcion_cliente == "1":
                informacion_nodo = crear_usuario_individuo(global_dpi)
                # print(create_node(session, informacion_nodo))

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
                update_info = actualizar_titulacion(global_dpi)
                print(update_relationship (session, update_info))

            elif opcion_cliente == "9":
                eliminar_usuario(global_dpi)

            elif opcion_cliente == "10":
                label, key_property, key_value = informacion_usuario(global_dpi)
                user_info = get_node_info(session, label, key_property, key_value)
                print_node_info(user_info)
                

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
