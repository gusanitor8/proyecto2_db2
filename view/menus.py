from utils.utils import *
from controller.db_crud import *

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
    nombre_empresa = input_null("Ingrese el nombre de la nueva empresa: ")
    nit = input_null("Ingrese el NIT de la empresa: ")
    direccion = input("Ingrese la dirección de la nueva empresa: ")
    regimen = input("Ingrese el régimen de la empresa: ")
    sector = input("Ingrese el sector de la empresa: ")
    telefono = input("Ingrese el número de teléfono de la empresa: ")
    email = input("Ingrese el correo electrónico de la empresa: ")
    representante = input_null("Ingrese el nombre del representante legal de la empresa: ")
    
    node_info = gen_node_struct(["Empresa"], 
                    {"nombre_empresa": nombre_empresa, 
                     "nit": nit,
                      "representate_legal": representante}, 
                     "nit", nit)
    if direccion:
        node_info["properties"]["direccion"] = direccion
    if regimen:
        node_info["properties"]["regimen"] = regimen
    if sector:
        node_info["properties"]["sector"] = sector
    if telefono:
        node_info["properties"]["telefono"] = telefono
    if email:
        node_info["properties"]["email"] = email
    
    return node_info

#3
def crear_cuenta(session):
    print("¿Qué tipo de cuenta deseas crear?")
    print("1. Cuenta de ahorro")
    print("2. Cuenta monetaria")
    print("3. Cuenta a plazos")

    tipo = input("Ingrese el número de la opción que deseas: ")
    no_cuenta = get_lates_account_number(session)
    no_cuenta = no_cuenta + 1
    saldo = input_float("Ingrese el saldo inicial de la cuenta: ")
    fecha_creacion = datetime.now()

    print("Seleccion la divisa de la cuenta: ")
    divisa_opt = input_int("1[USD] o 2[GTQ]")
    if divisa_opt == 1:
        divisa = "USD"
    elif divisa_opt == 2:
        divisa = "GTQ"
    else:
        divisa = "GTQ"
    
    estado = True

    
    if tipo == "1":
        type = 'Ahorro'
        limite = input_float("Ingrese el límite de la cuenta: ")
        interes = input_float("Ingrese el interés de la cuenta: ")
        objetivo = input("Ingrese el objetivo de la cuenta: (puede dejarlo en blanco)")

    elif tipo == "2":
        type = 'Monetaria'
        limite = input_float("Ingrese el límite de la cuenta: ")

    elif tipo == "3":
        type = 'Plazo'
        interes = input_float("Ingrese el interés de la cuenta: ")
        vencimiento = input_date("Ingrese la fecha de vencimiento de la cuenta: ")
        capital = saldo
        frecuencia = input_null("Ingrese la frecuencia de pago de la cuenta: ")

    node_info = gen_node_struct(["Cuenta", type], 
                    {"no_cuenta": no_cuenta, 
                     "saldo": saldo,
                     "fecha_apertura": fecha_creacion,
                     "divisa": divisa,
                     "estado": estado}, 
                     "no_cuenta", no_cuenta)
    if limite:
        node_info["properties"]["limite_retiro"] = limite
    if interes:
        node_info["properties"]["tasa_interes"] = interes
    if objetivo:
        node_info["properties"]["objetivo"] = objetivo
    if vencimiento:
        node_info["properties"]["vencimiento"] = vencimiento
    if capital:
        node_info["properties"]["capital_inicial"] = capital
    if frecuencia:
        node_info["properties"]["frecuencia_pago"] = frecuencia

    return node_info


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

#8 PENDIENTE
def actualizar_titulacion(global_dpi):
    dpi = input("Ingrese el DPI del usuario al que quiere cambiar la titulacion: ")
    nit = input("Ingrese el NIT de la empresa a la que quiere agregar la titularidad: ")

    node_info1 = {
        'labels': ["Individuo"],
        'properties': {
        "dpi": dpi
        },
        'key_property': "dpi",
        'key_value': dpi
    }

    node_info2 = {
        'labels': ["Empresa"],
        'properties': {
        "nit": nit
        },
        'key_property': "nit",
        'key_value': nit
    }

    relationship_type = 'TITULAR'

    property_value = input("Ingrese el nuevo valor para la propiedad de la relación (true or false): ")

    new_properties = {
        'estado': property_value
    }

    return node_info1, node_info2, relationship_type, new_properties

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
    dpi = input_int("Ingrese el DPI del usuario del que desea obtener información: ")

    label = 'Individuo'
    key_property = 'dpi'
    key_value = dpi
    
    return label, key_property, key_value
    

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