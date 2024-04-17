# Variables globales para almacenar DPI y NIT
global_dpi = None
global_nit = None

# Función para mostrar mensaje de éxito
def success_message(message):
    """Muestra un mensaje de éxito junto con un mensaje adicional.

    Args:
        message (str): Mensaje adicional que se mostrará junto al mensaje de éxito.
    """
    print("¡Éxito!", message)

# Función para mostrar el Menú 2 - Modo Administrador
def menu_administrador():
    global global_dpi

    print("\nSe ha ingresado como Usuario Administrador. \n¿Qué deseas realizar?")
    print("1. Desactivar cuenta de usuario o empresa")
    print("2. Clasificar cuentas de un usuario como fraudulentas")
    print("3. Editar la propiedad de fraude de una cuenta de usuario")
    print("4. Editar la propiedad de fraude de todas las cuentas de un usuario")
    print("5. Borrar la propiedad de fraude de una titulación o varias")

    opcion = input("Ingrese el número de la opción que deseas: ")

    if opcion == "1":
        print("\nHas seleccionado desactivar cuenta de usuario o empresa.")
        tipo = input("Elige para qué tipo de usuario deseas desactivar la cuenta (1: Usuario, 2: Empresa): ")
        if tipo == "1":
            print(input("Ingrese el DPI del usuario: "))
            print("Estas son las cuentas de ese usuario.")
            cuenta = input("Ingrese el No. de Cuenta que desea desactivar: ")
            success_message("La cuenta ha sido desactivada exitosamente.")
        elif tipo == "2":
            print(input("Ingrese el NIT de la empresa: "))
            success_message("La cuenta de la empresa ha sido desactivada exitosamente.")

    elif opcion == "2":
        print(input("Ingrese el DPI del usuario: "))
        print("Estas son las cuentas de ese usuario.")
        print("Seguro que desea marcar todas las cuentas como fraudulentas?")
        confirmacion = input("1. Si, 2. No: ")
        if confirmacion == "1":
            success_message("Todas las cuentas del usuario han sido marcadas como fraudulentas.")
        elif confirmacion == "2":
            print("No se han marcado las cuentas como fraudulentas.")
            # Que vuelva al menu anterior

    elif opcion == "3":
        print(input("Ingrese el DPI del usuario: "))
        print("Estas son las cuentas relacionadas al usuario.")
        cuenta = input("Ingrese el No. de Cuenta: ")
        fraude = input("Ingrese el nuevo valor para la propiedad de fraude: ")
        success_message("La propiedad de fraude ha sido actualizada exitosamente para la cuenta.")

    elif opcion == "4":
        print(input("Ingrese el DPI del usuario: "))
        print("Estas son las cuentas relacionadas al usuario.")
        fraude = input("Ingrese la nueva propiedad de fraude para todas las cuentas: ")
        success_message("Las propiedades de fraude han sido actualizadas exitosamente para todas las cuentas.")

    elif opcion == "5":
        print(input("Ingrese el DPI del usuario: "))
        print("Seguro que desea borrar la propiedad fraude para todas las titulaciones de este usuario?")
        confirmacion = input("1. Si, 2. No: ")
        if confirmacion == "1":
            success_message("La propiedad de fraude ha sido eliminada exitosamente.")
        elif confirmacion == "2":
            print("No se ha eliminado la propiedad de fraude.")
            # Que vuelva al menu anterior

# Función para mostrar el Menú 3 - Modo Cliente
def menu_cliente():
    global global_dpi

    print("\nSe ha ingresado como Usuario Cliente. ¿Qué deseas hacer?")
    print("1. Crear un usuario individuo")
    print("2. Crear un usuario empresa")
    print("3. Crear cuenta de ahorro, monetaria o a plazos asociada a un usuario")
    print("4. Agregar celular o correo a un usuario")
    print("5. Hacer una transferencia")
    print("6. Eliminar propiedades (celular o correo)")
    print("7. Actualizar celular o correo")
    print("8. Actualizar la titulación de los demás titulares")
    print("9. Eliminar usuario")
    print("10. Información de un usuario")
    print("11. Ver cuentas")
    print("12. Información de una cuenta")

    opcion = input("Ingrese el número de la opción que deseas: ")

    if opcion == "1":
        dpi = global_dpi
        nombre = input("Ingrese el nombre del nuevo usuario: ")
        edad = input("Ingrese la edad del nuevo usuario: ")
        direccion = input("Ingrese la dirección del nuevo usuario: ")
        success_message("El usuario individuo ha sido creado exitosamente.")

    elif opcion == "2":
        dpi = global_dpi
        nit = global_nit
        nombre_empresa = input("Ingrese el nombre de la nueva empresa: ")
        direccion_empresa = input("Ingrese la dirección de la nueva empresa: ")
        success_message("La empresa ha sido creada exitosamente.")

    elif opcion == "3":
        dpi = global_dpi
        balance = input("Ingrese el balance inicial de la cuenta: ")
        success_message("La cuenta ha sido creada exitosamente.")

    elif opcion == "4":
        dpi = global_dpi
        print("Qué desea agregar?")
        opcion_agregar = input("1. Celular, 2. Correo: ")
        if opcion_agregar == "1":
            celular = input("Ingrese el número de celular: ")
            success_message("El número de celular ha sido agregado exitosamente.")
        elif opcion_agregar == "2":
            correo = input("Ingrese la dirección de correo electrónico: ")
            success_message("La dirección de correo electrónico ha sido agregada exitosamente.")

    elif opcion == "5":
        dpi = global_dpi
        print("Estas son sus cuentas:")
        cuenta_origen = input("Ingrese el No. de Cuenta desde la que desea realizar la transferencia: ")
        cuenta_destino = input("Ingrese el No. de Cuenta al que desea transferir: ")
        monto = input("Ingrese el monto a transferir: ")
        success_message("La transferencia se ha realizado exitosamente.")

    elif opcion == "6":
        dpi = global_dpi
        print("Qué desea eliminar?")
        opcion_eliminar = input("1. Celular, 2. Correo: ")
        if opcion_eliminar == "1":
            success_message("El número de celular ha sido eliminado exitosamente.")
        elif opcion_eliminar == "2":
            success_message("La dirección de correo electrónico ha sido eliminada exitosamente.")

    elif opcion == "7":
        dpi = global_dpi
        print("Qué desea actualizar?")
        opcion_actualizar = input("1. Celular, 2. Correo: ")
        if opcion_actualizar == "1":
            nuevo_celular = input("Ingrese el nuevo número de celular: ")
            success_message("El número de celular ha sido actualizado exitosamente.")
        elif opcion_actualizar == "2":
            nuevo_correo = input("Ingrese la nueva dirección de correo electrónico: ")
            success_message("La dirección de correo electrónico ha sido actualizada exitosamente.")

    elif opcion == "8":
        dpi = global_dpi
        print("Ingrese la nueva titulación para este usuario.")

    elif opcion == "9":
        print("Esta seguro que quiere eliminar su usuario?")
        confirmacion = input("1. Si, 2. No: ")
        if confirmacion == "1":
            dpi = global_dpi
            success_message("El usuario ha sido eliminado exitosamente.")
        elif confirmacion == "2":
            print("No se ha eliminado el usuario.")
            # Que vuelva al menu anterior
    
    elif opcion == "10":
        dpi = global_dpi
        print("Esta es la información de su usuario.")

    elif opcion == "11":
        dpi = global_dpi
        print("Estas son sus cuentas.")

# Función para mostrar el Menú 1
def menu_principal():
    global global_dpi
    global global_nit

    print("Bienvenido a nuestra banca. ¿Cómo deseas entrar?")
    print("1. Modo Administrador")
    print("2. Modo Cliente")

    opcion = input("Ingrese el número de la opción que deseas: ")

    if opcion == "1":
        menu_administrador()
    elif opcion == "2":
        global_dpi = input("Ingrese su DPI: ")
        global_nit = input("Ingrese su NIT: ")
        menu_cliente()

# Programa principal
menu_principal()
