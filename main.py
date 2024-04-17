from controller.db_connection import *
from controller.db_crud import *
from controller.csv_processing import *

try:

    driver = get_driver()
    with driver.session() as session:
        user = get_node_info(session, 'Individuo', 'dpi', 5)
        print('INFO: Node information retrieved successfully')
        print_node_info(user)
        cuentas = find_associated_accounts(session, 'Individuo', 'dpi', 5)
        print('INFO: Associated accounts retrieved successfully')
        for cuenta in cuentas:
            print_node_info(cuenta)
            print('Transacciones salientes:')
            transaction_history(session, cuenta['properties']['no_cuenta'])
            print('Transacciones entrantes:')
            incoming_transaction_history(session, cuenta['properties']['no_cuenta'])
        trans_id = int(input('Ingrese el codigo de la transaccion a consultar: '))
        transaccion = find_transaction_by_id(session, trans_id)

        tipo_trans = 'Pago'
        handle_transaction(session, tipo_trans)
        

except Exception as e:
    print(f"ERROR: {e}")

finally:
    close_driver()