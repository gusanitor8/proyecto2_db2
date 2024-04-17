def node_exists(session, labels, key_property, value):
    """
    Check if a node with the specified label and key property exists.
    
    Args:
    - session: A Neo4j session object.
    - label: The label of the node.
    - key_property: The key property name of the node.
    - value: The value of the key property.

    Returns:
    - True if the node exists, False otherwise.
    """
    query = f"MATCH (n:{labels}) WHERE n.{key_property} = $value RETURN count(n) > 0 AS exists"
    result = session.run(query, value=value)
    exists = result.single()[0]
    return exists


def create_node(session, labels, properties, key_property):
    """
    Create a new node with the given label and properties if it does not already exist, using the specified key property for existence check.
    
    Args:
    - session: A Neo4j session object.
    - label: The label of the node.
    - properties: A dictionary of properties for the node.
    - key_property: The key property name to check for existence.
    
    Returns:
    - A message indicating the outcome of the operation.
    """
    if key_property not in properties:
        raise ValueError ("Key property not found in properties.")

    value = properties[key_property]
    if node_exists(session, labels, key_property, value):
        raise ValueError (f"Node {value} already exists.")
    
    properties_string = ', '.join([f"{k}: ${k}" for k in properties])
    query = f"CREATE (n:{labels} {{{properties_string}}}) RETURN n"
    result = session.run(query, **properties)
    return f"SUCCESS: Node {value} created successfully."



