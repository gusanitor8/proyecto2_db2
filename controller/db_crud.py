from datetime import datetime

"""
Structure of node_info:
{
    'labels': ['Label1', 'Label2'],  # List of labels to apply to the node
    'properties': {                  # Dictionary of properties for the node
        'property1': 'value1',
        'property2': 'value2',
        ...                          # Add as many properties as needed
    },
    'key_property': 'property1',     # The key property to identify the node uniquely
    'key_value': 'value1'            # The value of the key property to identify the node uniquely
}
"""


def find_node(session, node_info):
    """
    Finds a node in the database based on the provided node_info.

    Args:
        session: The Neo4j session object.
        node_info: A dictionary containing information about the node to find. It should have the following keys:
            - 'labels': A list of labels associated with the node.
            - 'key_property': The property used as the key to find the node.
            - 'key_value': The value of the key property to search for.

    Returns:
        bool: True if the node exists, False otherwise.
    """
    label_string = ":".join(node_info['labels'])
    query = f"MATCH (n:{label_string}) WHERE n.{node_info['key_property']} = $key_value RETURN count(n) > 0 AS exists"
    result = session.run(query, key_value=node_info['key_value'])
    exists = result.single()[0]
    return exists


def create_node(session, node_info):
    """
    Creates a node in the database with the given session and node information.

    Parameters:
    - session: The session object used to interact with the database.
    - node_info: A dictionary containing the information of the node to be created.
                             It should have the following keys:
                             - 'labels': A list of labels to be assigned to the node.
                             - 'properties': A dictionary of properties to be assigned to the node.
                                                             The keys are the property names and the values are the property values.
                             - 'key_property': The name of the property used as the key to check if the node already exists.
                             - 'key_value': The value of the key property used to check if the node already exists.

    Returns:
    - A string indicating the result of the operation. If the node is created successfully, it returns
        "SUCCESS: Node with {key_property}='{key_value}' created successfully.".
        If the node already exists, it raises a RuntimeError with the message
        "Node with {key_property} = '{key_value}' already exists."
    """
    if find_node(session, node_info):
        raise RuntimeError(f"Node with {node_info['key_property']} = '{node_info['key_value']}' already exists.")

    label_string = ":".join(node_info['labels'])
    properties_string = ', '.join([f"{k}: ${k}" for k in node_info['properties']])
    query = f"CREATE (n:{label_string} {{{properties_string}}}) RETURN n"
    result = session.run(query, **node_info['properties'])
    return f"SUCCESS: Node with {node_info['key_property']}='{node_info['key_value']}' created."


def create_relationship(session, node1_info, node2_info, relationship_type, relationship_properties=None):
    """
    Creates a relationship between two nodes in the database.

    Args:
        session: The Neo4j session object.
        node1_info: A dictionary containing information about the first node.
        node2_info: A dictionary containing information about the second node.
        relationship_type: The type of relationship to create.
        relationship_properties: (optional) A dictionary of properties to set on the relationship.

    Returns:
        A success message if the relationship is created successfully.

    Raises:
        RuntimeError: If one or both nodes do not exist or if the relationship creation fails.
    """
    if not find_node(session, node1_info) or not find_node(session, node2_info):
        raise RuntimeError("One or both nodes do not exist.")

    query = (
        f"MATCH (a:{':'.join(node1_info['labels'])} {{{node1_info['key_property']}: $node1_value}}), "
        f"(b:{':'.join(node2_info['labels'])} {{{node2_info['key_property']}: $node2_value}}) "
        f"CREATE (a)-[r:{relationship_type} $rel_properties]->(b) "
        f"RETURN type(r)"
    )
    params = {
        'node1_value': node1_info['key_value'],
        'node2_value': node2_info['key_value'],
        'rel_properties': relationship_properties or {}
    }
    result = session.run(query, **params)
    if result.single():
        return f"SUCCESS: Relationship {relationship_type} created between {node1_info['key_value']} and {node2_info['key_value']}."
    else:
        raise RuntimeError("Failed to create relationship.")


def update_node_properties(session, node_info):
    def make_query(node_info):
        query = f"MERGE (n:{':'.join(node_info['labels'])} {{ {node_info['key_property']}: $key_value }}) "
        query += f"ON MATCH SET {', '.join([f'n.{k} = ${k}' for k in node_info['properties']])}"
        return query

    query = make_query(node_info)
    result = session.run(query, key_value=node_info['key_value'], **node_info['properties'])
    return f"SUCCESS: Node with {node_info['key_property']}='{node_info['key_value']}' updated."

def update_relationship(session, node1_info, node2_info, relationship_type, new_properties):
    """
    Updates a relationship between two nodes in the database.

    Args:
        session: The Neo4j session object.
        node1_info: A dictionary containing information about the first node.
        node2_info: A dictionary containing information about the second node.
        relationship_type: The type of relationship to update.
        new_properties: A dictionary of properties to update on the relationship.

    Returns:
        A success message if the relationship is updated successfully.

    Raises:
        RuntimeError: If one or both nodes do not exist or if the relationship update fails.
    """
    if not find_node(session, node1_info) or not find_node(session, node2_info):
        raise RuntimeError("One or both nodes do not exist.")

    properties_string = ', '.join([f"r.{k} = ${k}" for k in new_properties])
    query = (
        f"MATCH (a:{':'.join(node1_info['labels'])} {{{node1_info['key_property']}: $node1_value}})-"
        f"[r:{relationship_type}]->"
        f"(b:{':'.join(node2_info['labels'])} {{{node2_info['key_property']}: $node2_value}}) "
        f"SET {properties_string} "
        f"RETURN type(r)"
    )
    params = {
        'node1_value': node1_info['key_value'],
        'node2_value': node2_info['key_value'],
        **new_properties
    }
    result = session.run(query, **params)
    if result.single():
        return f"SUCCESS: Relationship {relationship_type} updated between {node1_info['key_value']} and {node2_info['key_value']}."
    else:
        raise RuntimeError("Failed to update relationship.")


def get_node_info(session, label, key_property, key_value):
    query = f"MATCH (n:{label}) WHERE n.{key_property} = $key_value RETURN labels(n) AS labels, properties(n) AS properties"
    result = session.run(query, key_value=key_value)
    node = result.single()

    if node:
        labels, properties = node['labels'], node['properties']
        return {
            'labels': labels,
            'properties': properties,
            'key_property': key_property,
            'key_value': properties.get(key_property)
        }
    else:
        raise ValueError(f"No node found with {key_property} = '{key_value}'")


def print_node_info(node_info):
    print('Detalles de', " ".join(node_info['labels']))
    for key, value in node_info['properties'].items():
        if isinstance(value, str) and '\n' in value:
            value = value.replace('\n', ', ')
        print(f"- {key}: {value}")
    print()


def find_associated_accounts(session, node_label, key_property, key_value):
    query = f"""
    MATCH (n:{node_label})-[r:TITULAR]->(c:Cuenta)
    WHERE n.{key_property} = $key_value
    RETURN labels(c) AS labels, properties(c) AS properties
    """
    results = session.run(query, key_value=key_value)
    accounts = []

    for record in results:
        account_info = {
            'labels': record['labels'],
            'properties': record['properties']
        }
        accounts.append(account_info)

    return accounts


def print_transaction_info(transaction):
    print(f"Codigo: {transaction.id}")
    for key, value in transaction.items():
        if isinstance(value, str) and '\n' in value:
            value = value.replace('\n', ', ')
        print(f"  - {key}: {value}")
    print()


def transaction_history(session, account_number):
    skip = 0
    limit = 3  # Define el límite de transacciones por página

    while True:
        query = """
        MATCH (c:Cuenta {no_cuenta: $account_number})-[r:TRANSACCION]->(c2:Cuenta)
        RETURN r, c2.no_cuenta AS cuenta_destino ORDER BY r.fecha DESC SKIP $skip LIMIT $limit
        """
        results = session.run(query, account_number=account_number, skip=skip, limit=limit)
        transactions = list(results)

        if not transactions:
            print(
                "Ha visto todas las transacciones de su cuenta." if skip != 0 else "No hay transacciones disponibles para esta cuenta.")
            break

        for record in transactions:
            print(f"Transacción a la cuenta: {record['cuenta_destino']}")
            print_transaction_info(record['r'])

        if len(transactions) < limit:
            print("Ha visto todas las transacciones de su cuenta.\n")
            break

        if input("Desea ver más transacciones? (s/n): ").lower() != 's':
            break
        skip += limit


def incoming_transaction_history(session, account_number):
    skip = 0
    limit = 3  # Define el límite de transacciones por página

    while True:
        query = """
        MATCH (c1:Cuenta)-[r:TRANSACCION]->(c:Cuenta {no_cuenta: $account_number})
        RETURN r, c1.no_cuenta AS cuenta_origen ORDER BY r.fecha DESC SKIP $skip LIMIT $limit
        """
        results = session.run(query, account_number=account_number, skip=skip, limit=limit)
        transactions = list(results)

        if not transactions:
            print(
                "Ha visto todas las transacciones entrantes de su cuenta." if skip != 0 else "No hay transacciones entrantes disponibles para esta cuenta.")
            break

        for record in transactions:
            print(f"Transacción desde la cuenta: {record['cuenta_origen']}")
            print_transaction_info(record['r'])

        if len(transactions) < limit:
            print("Ha visto todas las transacciones entrantes de su cuenta.\n")
            break

        if input("Desea ver más transacciones entrantes? (s/n): ").lower() != 's':
            break
        skip += limit


def find_transaction_by_id(session, transaction_id):
    query = """
    MATCH ()-[r:TRANSACCION]->() WHERE id(r) = $transaction_id
    RETURN r, id(r) AS id, startNode(r).no_cuenta AS cuenta_origen, endNode(r).no_cuenta AS cuenta_destino
    """
    result = session.run(query, transaction_id=transaction_id)
    record = result.single()

    if record:
        transaction_info = {
            'id': record['id'],
            'cuenta_origen': record['cuenta_origen'],
            'cuenta_destino': record['cuenta_destino'],
            'properties': dict(record['r'])
        }
        print(f"Transaccion desde la cuenta {record['cuenta_origen']} a la cuenta {record['cuenta_destino']}:")
        print_transaction_info(record['r'])

        return transaction_info
    else:
        raise ValueError("No se encontró la transacción con el ID proporcionado.")


def handle_transaction(session, transaction_type='TRANSFERENCIA'):
    # Solicitar información de la transacción
    from_account = int(input("Ingrese el número de la cuenta origen: "))
    from_account_info = get_node_info(session, 'Cuenta', 'no_cuenta', from_account)
    to_account = int(input("Ingrese el número de la cuenta destino: "))
    to_account_info = get_node_info(session, 'Cuenta', 'no_cuenta', to_account)
    amount = float(input("Ingrese el monto de la transacción: "))
    description = input("Ingrese una descripción para la transacción (puede dejarlo en blanco): ")
    ubicacion = input("Ingrese la ubicación de la transacción (puede dejarlo en blanco): ")

    # Verificar condiciones de saldo y límite de retiro
    if amount > from_account_info['properties']['saldo'] or amount > from_account_info['properties']['limite_retiro']:
        raise ValueError("La transacción excede el límite de retiro o el saldo disponible.")

    # Preparar las propiedades de la transacción, excluyendo las vacías
    transaction_properties = {
        'monto': amount,
        'fecha': datetime.now(),
        'tipo': transaction_type,
        'alerta': False
    }

    if description:  # Solo añadir descripción si no está vacía
        transaction_properties['descripcion'] = description
    if ubicacion:
        transaction_properties['ubicacion'] = ubicacion

    # Crear la relación de transacción
    create_relationship(session, from_account_info, to_account_info, 'TRANSACCION', transaction_properties)

    # Actualizar saldos
    update_account_balance(session, from_account, -amount)
    update_account_balance(session, to_account, amount)
    print("Transacción realizada con éxito.")


def update_account_balance(session, account_number, amount_change):
    query = f"MATCH (c:Cuenta {{no_cuenta: $account_number}}) SET c.saldo = c.saldo + $amount_change RETURN c.saldo"
    result = session.run(query, account_number=account_number, amount_change=amount_change)
    return result.single()[0]
