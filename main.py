from controller.db_connection import *
from controller.db_crud import *
from controller.csv_processing import *

try:

    test_dic = {
        'labels': ['Individuo'],
            'properties': {
                'telefono': '45801692',
                'email': 'gusanitor8'
            },
        'key_property': 'dpi',
        'key_value': 6.0
    }

    driver = get_driver()
    with driver.session() as session:
        update_node_properties(session, test_dic)
        

except Exception as e:
    print(f"ERROR: {e}")

finally:
    close_driver()