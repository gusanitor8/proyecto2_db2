from controller.db_connection import *
from controller.db_crud import *
from controller.csv_processing import *
from view.view_graph import display_trans_history

# try:

node1_dic = {
    'labels': ['Empresa'],
    'key_property': 'nit',
    'key_value': 9.0
}

node2_dic = {
    'labels': ['Cuenta'],
    'key_property': 'no_cuenta',
    'key_value': 1.0
}

rel_type = 'TITULAR'

rel_properties = {
    'pruebita': 'hola!!'
}


driver = get_driver()
with driver.session() as session:
    display_trans_history(session, node2_dic)
        

# except Exception as e:
#     print(f"ERROR: {e}")
#
# finally:
#     close_driver()