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


def inpt_null(message):
    while True:
        value = input(message)
        if value == "":
            print("Por favor, ingrese un valor válido.")
        else:
            return value