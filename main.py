from controller.db_connection import *
from controller.db_crud import *

try:
    driver = get_driver()
    with driver.session() as session:
        node1_info = {
            'labels': ['Person', 'Employee'],
            'properties': {'name': 'Alice', 'age': 30},
            'key_property': 'name',
            'key_value': 'Alice'
        }

        node2_info = {
            'labels': ['Project'],
            'properties': {'name': 'Neptune', 'description': 'Deep Learning'},
            'key_property': 'name',
            'key_value': 'Neptune'
        }
        node3_info = {
            'labels': ['Project'],
            'properties': {'name': 'XD', 'description': 'Dxdg'},
            'key_property': 'name',
            'key_value': 'XD'
        }
        relationship_type = 'WORKS_ON'
        relationship_properties = {'since': '2020'}

        print(create_node(session, node1_info))
        print(create_node(session, node2_info))
        print(create_relationship(session, node1_info, node2_info, relationship_type, relationship_properties))
        print(create_relationship(session, node1_info, node3_info, relationship_type, relationship_properties))


except Exception as e:
    print(f"ERROR: {e}")

finally:
    close_driver()