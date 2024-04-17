from utils.utils import *

def success_message(message):
    """Muestra un mensaje de éxito junto con un mensaje adicional.

    Args:
        message (str): Mensaje adicional que se mostrará junto al mensaje de éxito.
    """
    print("¡Éxito!", message)

def menu_principal ():
    print("\n----------------------------------------------------")
    print("Bienvenido a nuestra banca. ¿Cómo deseas entrar?")
    print("1. Modo Administrador")
    print("2. Modo Cliente")
    print("3. Salir")

    opcion = input("Ingrese el número de la opción que deseas: ")

    return opcion


# ADMINISTRADOR
def modo_administrador():
    while True:
        try:
            print("\nSe ha ingresado como Usuario Administrador. \n¿Qué deseas realizar?")
            print("1. Desactivar cuenta de usuario o empresa")
            print("2. Clasificar cuentas de un usuario como fraudulentas")
            print("3. Editar la propiedad de fraude de una cuenta de usuario")
            print("4. Editar la propiedad de fraude de todas las cuentas de un usuario")
            print("5. Borrar la propiedad de fraude de una titulación o varias")
            print("6. Regresar al menú principal")
    
            opcion = input("Ingrese el número de la opción que deseas: ")
    
            if opcion not in ["1", "2", "3", "4", "5", "6"]:
                raise ValueError("Opción inválida. Por favor ingresa un número del 1 al 5.")
            
            return opcion
        except ValueError as e:
            print("Error:", e)

def desactivar_cuenta():
    tipo = input("Elige para qué tipo de usuario deseas desactivar la cuenta (1: Usuario, 2: Empresa): ")
    if tipo == "1":
        print(input("Ingrese el DPI del usuario: "))
        print("Estas son las cuentas de ese usuario.")
        cuenta = input("Ingrese el No. de Cuenta que desea desactivar: ")
        success_message("La cuenta ha sido desactivada exitosamente.")
        modo_administrador()  # Regresar al menú anterior
    elif tipo == "2":
        print(input("Ingrese el NIT de la empresa: "))
        success_message("La cuenta de la empresa ha sido desactivada exitosamente.")
        modo_administrador()  # Regresar al menú anterior

def clasificar_cuentas_fraudulentas():
    print(input("Ingrese el DPI del usuario: "))
    print("Estas son las cuentas de ese usuario.")
    print("Seguro que desea marcar todas las cuentas como fraudulentas?")
    confirmacion = input("1. Si, 2. No: ")
    if confirmacion == "1":
        success_message("Todas las cuentas del usuario han sido marcadas como fraudulentas.")
        modo_administrador()  # Regresar al menú anterior
    elif confirmacion == "2":
        print("No se han marcado las cuentas como fraudulentas.")
        modo_administrador()  # Regresar al menú anterior

def marcar_cuenta_fraudulenta():
    print(input("Ingrese el DPI del usuario: "))
    print("Estas son las cuentas relacionadas al usuario.")
    cuenta = input("Ingrese el No. de Cuenta: ")
    fraude = input("Ingrese el nuevo valor para la propiedad de fraude: ")
    success_message("La propiedad de fraude ha sido actualizada exitosamente para la cuenta.")
    modo_administrador()  # Regresar al menú anterior

def marcar_cuentas_fraudulentas():
    print(input("Ingrese el DPI del usuario: "))
    print("Estas son las cuentas relacionadas al usuario.")
    fraude = input("Ingrese la nueva propiedad de fraude para todas las cuentas: ")
    success_message("Las propiedades de fraude han sido actualizadas exitosamente para todas las cuentas.")
    modo_administrador()  # Regresar al menú anterior

def borrar_propiedad_fraude():
    print(input("Ingrese el DPI del usuario: "))
    print("Seguro que desea borrar la propiedad fraude para todas las titulaciones de este usuario?")
    confirmacion = input("1. Si, 2. No: ")
    if confirmacion == "1":
        success_message("La propiedad de fraude ha sido eliminada exitosamente.")
        modo_administrador()  # Regresar al menú anterior
    elif confirmacion == "2":
        print("No se ha eliminado la propiedad de fraude.")
        modo_administrador()  # Regresar al menú anterior

# CLIENTE
def modo_cliente():
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
    print("13. Regresar al menú principal")

    opcion = input("Ingrese el número de la opción que deseas: ")

    return opcion

#1
def crear_usuario_individuo():
    nombre = input("Ingrese el nombre del nuevo usuario: ")
    edad = input_int("Ingrese la edad del nuevo usuario: ")
    dpi = input_int("Ingrese el DPI del nuevo usuario: ")
    nit = input("Ingrese el NIT del nuevo usuario: (puede dejarlo en blanco)")
    direccion = input("Ingrese la dirección del nuevo usuario: (puede dejarlo en blanco)")
    telefono = input("Ingrese el número de teléfono del nuevo usuario: (puede dejarlo en blanco)")
    email = input("Ingrese el correo electrónico del nuevo usuario: (puede dejarlo en blanco)")
    
    node_info = gen_node_struct(["Individuo"], 
                    {"nombre": nombre, 
                     "dpi": dpi, }, 
                     "dpi", dpi)
    if edad:
        node_info["properties"]["edad"] = edad
    if nit:
        node_info["properties"]["nit"] = nit
    if direccion:
        node_info["properties"]["direccion"] = direccion
    if telefono:
        node_info["properties"]["telefono"] = telefono
    if email:
        node_info["properties"]["email"] = email

    return node_info


#2
def crear_usuario_empresa():
    nit = input("Ingrese el NIT de la empresa: ")
    nombre_empresa = input("Ingrese el nombre de la nueva empresa: ")
    direccion_empresa = input("Ingrese la dirección de la nueva empresa: ")
    success_message("La empresa ha sido creada exitosamente.")
    menu_principal()  # Regresar al menú principal

#3
def crear_cuenta(global_dpi):
    print("¿Qué tipo de cuenta deseas crear?")
    print("1. Cuenta de ahorro")
    print("2. Cuenta monetaria")
    print("3. Cuenta a plazos")

    tipo = input("Ingrese el número de la opción que deseas: ")

    if tipo == "1":
        dpi = global_dpi
        balance = input("Ingrese el balance inicial de la cuenta: ")
        print("Creando cuenta de ahorro...")
        success_message("La cuenta de ahorro ha sido creada exitosamente.")
        modo_cliente()
    elif tipo == "2":
        dpi = global_dpi
        balance = input("Ingrese el balance inicial de la cuenta: ")
        print("Creando cuenta monetaria...")
        success_message("La cuenta monetaria ha sido creada exitosamente.")
        modo_cliente()
    elif tipo == "3":
        dpi = global_dpi
        balance = input("Ingrese el balance inicial de la cuenta: ")
        print("Creando cuenta a plazos...")
        success_message("La cuenta a plazos ha sido creada exitosamente.")
        modo_cliente()

#4
def agregar_celular_correo(global_dpi):
    dpi = global_dpi
    print("Qué desea agregar?")
    opcion_agregar = input("1. Celular, 2. Correo: ")
    if opcion_agregar == "1":
        celular = input("Ingrese el número de celular: ")
        success_message("El número de celular ha sido agregado exitosamente.")
        menu_principal()  # Regresar al menú principal
    elif opcion_agregar == "2":
        correo = input("Ingrese la dirección de correo electrónico: ")
        success_message("La dirección de correo electrónico ha sido agregada exitosamente.")
        menu_principal()  # Regresar al menú principal

#5
def hacer_transferencia(global_dpi):
    dpi = global_dpi
    print("Estas son sus cuentas:")
    cuenta_origen = input("Ingrese el No. de Cuenta desde la que desea realizar la transferencia: ")
    cuenta_destino = input("Ingrese el No. de Cuenta a la que desea transferir: ")
    monto = input("Ingrese el monto a transferir: ")
    success_message("La transferencia se ha realizado exitosamente.")
    menu_principal()  # Regresar al menú principal

#6
def eliminar_propiedades(global_dpi):
    dpi = global_dpi
    print("Qué desea eliminar?")
    opcion_eliminar = input("1. Celular, 2. Correo: ")
    if opcion_eliminar == "1":
        success_message("El número de celular ha sido eliminado exitosamente.")
        menu_principal()  # Regresar al menú principal
    elif opcion_eliminar == "2":
        success_message("La dirección de correo electrónico ha sido eliminada exitosamente.")
        menu_principal()  # Regresar al menú principal

#7
def actualizar_celular_correo(global_dpi):
    dpi = global_dpi
    print("Qué desea actualizar?")
    opcion_actualizar = input("1. Celular, 2. Correo: ")
    if opcion_actualizar == "1":
        nuevo_celular = input("Ingrese el nuevo número de celular: ")
        success_message("El número de celular ha sido actualizado exitosamente.")
        menu_principal()  # Regresar al menú principal
    elif opcion_actualizar == "2":
        nuevo_correo = input("Ingrese la nueva dirección de correo electrónico: ")
        success_message("La dirección de correo electrónico ha sido actualizada exitosamente.")
        menu_principal()  # Regresar al menú principal

#8
def actualizar_titulacion(global_dpi):
    dpi = global_dpi
    print("Ingrese la nueva titulación para este usuario.")
    success_message("La titulación ha sido actualizada exitosamente.")
    menu_principal()  # Regresar al menú principal

#9
def eliminar_usuario(global_dpi):
    print("Esta seguro que quiere eliminar su usuario?")
    confirmacion = input("1. Si, 2. No: ")
    if confirmacion == "1":
        dpi = global_dpi
        success_message("El usuario ha sido eliminado exitosamente.")
        menu_principal()  # Regresar al menú principal
    elif confirmacion == "2":
        print("No se ha eliminado el usuario.")
        menu_principal()  # Regresar al menú anterior

#10
def informacion_usuario(global_dpi):
    dpi = global_dpi
    print("Esta es la información de su usuario.")
    menu_principal()  # Regresar al menú principal

#11
def ver_cuentas(global_dpi):
    dpi = global_dpi
    print("Estas son sus cuentas.")
    menu_principal()  # Regresar al menú principal

#12
def informacion_cuenta(global_dpi):
    dpi = global_dpi
    print("Estas son sus cuentas.")
    cuenta = input("Ingrese el No. de Cuenta de la que desea obtener informacion: ")
    print("Esta es la información de la cuenta.")
    menu_principal()  # Regresar al menú principal