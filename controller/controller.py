from view.menus import *
from controller.controller_functions import deactivate_user_accounts, mark_account_as_fraud, \
    edit_fraud_for_user_accounts, rm_fraud_prop_from_user_titulations, edit_fraude_in_titulacion, display_trans_history_
from controller.db_crud import *
from utils.utils import *

global_dpi = ""


def run(session):
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

            elif opcion_administrador == "8":
                account = get_cuenta()
                display_trans_history_(account)


        # Cliente
        elif opcion_principal == "2":

            global_dpi = input_int("Ingrese su DPI: ")

            opcion_cliente = modo_cliente()

            if opcion_cliente == "1":
                informacion_nodo = crear_usuario_individuo()
                print(create_node(session, informacion_nodo))


            elif opcion_cliente == "2":
                info_nodo = crear_usuario_empresa()
                print(create_node(session, info_nodo))


            elif opcion_cliente == "3":
                info_nodo = crear_cuenta(session)
                print(create_node(session, info_nodo))

            elif opcion_cliente == "4":
                agregar_celular_correo(global_dpi, session)

            elif opcion_cliente == "5":
                hacer_transferencia(session)

            elif opcion_cliente == "6":
                eliminar_propiedades(session)

            elif opcion_cliente == "7":
                actualizar_celular_correo(session)

            elif opcion_cliente == "8":
               actualizar_titulacion(session)

            elif opcion_cliente == "9":
                label, key_property, key_value = eliminar_usuario(global_dpi)
                user_info = get_node_info(session, label, key_property, key_value)
                print(delete_node(session, user_info))

            elif opcion_cliente == "10":
                label, key_property, key_value = informacion_usuario(global_dpi)
                user_info = get_node_info(session, label, key_property, key_value)
                print_node_info(user_info)
                

            elif opcion_cliente == "11":
                node_label, key_property, key_value = ver_cuentas(global_dpi)
                print(find_associated_accounts(session, node_label, key_property, key_value))

            elif opcion_cliente == "12":
                node_label, key_property, key_value = ver_cuentas(global_dpi)
                print(find_associated_accounts(session, node_label, key_property, key_value))

                label, key_property, key_value = informacion_cuenta(global_dpi)
                cuenta_info = get_node_info(session, label, key_property, key_value)
                print_node_info(cuenta_info)

            elif opcion_cliente == "13":
                print("Regresando al menú principal...")
                print("")
                menu_principal(global_dpi)




        # Salir
        elif opcion_principal == "3":
            print("Gracias por utilizar nuestros servicios. ¡Hasta luego!")
            print("")
            exit()
