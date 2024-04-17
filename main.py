from controller.controller import run
from controller.db_crud import delete_node
from controller.db_connection import *


if __name__ == "__main__":
#     run()
    node_info = {
        'labels': ['Individuo'],
        'key_property': 'dpi',
        'key_value': 5
    }

    try:
        driver = get_driver()
        with driver.session() as session:
            delete_node(session, node_info)
    except Exception as e:
        print(f'Failed to delete node: {e}')
    finally:
        close_driver()

