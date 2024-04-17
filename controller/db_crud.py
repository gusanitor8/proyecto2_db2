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
