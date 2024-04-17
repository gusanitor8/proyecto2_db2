from datetime import datetime

def input_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Por favor, ingrese un número entero válido.")


def input_float(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Por favor, ingrese un número válido.")

def gen_node_struct(labels, properties, key, value):
    node_info = {
        "labels":labels,
        "properties":dict(properties),
        "key_property":key,
        "key_value":value
    }
    return node_info


def input_null(message):
    while True:
        value = input(message)
        if value == "":
            print("Por favor, ingrese un valor válido.")
        else:
            return value
        
def input_date(message):
    while True:
        try:
            date = input(message)
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Por favor, ingrese una fecha válida (YYYY-MM-DD).")