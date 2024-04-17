from controller.db_crud import *
from controller.db_connection import *
from view.view_graph import display_trans_history


def deactivate_user_accounts(dpi_or_nit, is_dpi: bool):
    try:
        driver = get_driver()
        with driver.session() as session:
            accounts = get_user_accounts(session, dpi_or_nit, is_dpi=is_dpi)

            for account_no in accounts:
                node_info = {
                    'labels': ['Cuenta'],
                    'properties': {
                        'estado': False
                    },
                    'key_property': 'no_cuenta',
                    'key_value': account_no
                }

                update_node_properties(session, node_info)

            print('INFO: Successfully deactivated user accounts')

    except Exception as e:
        raise RuntimeError(f'Failed to deactivate user accounts: {e}')
    finally:
        close_driver()


def mark_account_as_fraud(account_no: int, is_fraud=True):
    try:
        driver = get_driver()
        with driver.session() as session:
            node_info = {
                'labels': ['Cuenta'],
                'properties': {
                    'fraudulenta': is_fraud
                },
                'key_property': 'no_cuenta',
                'key_value': account_no
            }

            update_node_properties(session, node_info)

            if is_fraud:
                print('INFO: Successfully marked account as fraud')
            else:
                print('INFO: Successfully unmarked account as fraud')

    except Exception as e:
        raise RuntimeError(f'Failed to mark account as fraud: {e}')
    finally:
        close_driver()


def delete_fraud_property(account_no):
    try:
        driver = get_driver()
        with driver.session() as session:
            node_info = {
                'labels': ['Cuenta'],
                'key_property': 'no_cuenta',
                'key_value': account_no
            }
            property_to_remove = 'fraudulenta'

            remove_node_property(session, node_info, property_to_remove)
            print('INFO: Successfully deleted fraud property')

    except Exception as e:
        raise RuntimeError(f'Failed to delete fraud property: {e}')
    finally:
        close_driver()


def edit_fraud_for_user_accounts(dpi_or_nit, is_fraud: bool, is_dpi=True):
    try:
        driver = get_driver()
        with driver.session() as session:
            accounts = get_user_accounts(session, dpi_or_nit, is_dpi=is_dpi)

            for account_no in accounts:
                node_info = {
                    'labels': ['Cuenta'],
                    'properties': {
                        'fraudulenta': is_fraud
                    },
                    'key_property': 'no_cuenta',
                    'key_value': account_no
                }

                update_node_properties(session, node_info)

            print('INFO: Successfully edited fraud property for user accounts')

    except Exception as e:
        raise RuntimeError(f'Failed to mark user accounts as fraud: {e}')
    finally:
        close_driver()


def rm_fraud_prop_from_user_titulations(dpi_or_nit, is_dpi: bool = True):
    try:
        driver = get_driver()
        with driver.session() as session:

            accounts = get_user_accounts(session, dpi_or_nit, is_dpi=is_dpi)

            if is_dpi:
                node_info = {
                    'labels': ['Individuo'],
                    'key_property': 'dpi',
                    'key_value': dpi_or_nit
                }
            else:
                node_info = {
                    'labels': ['Empresa'],
                    'key_property': 'nit',
                    'key_value': dpi_or_nit
                }

            for account_no in accounts:
                node_info_acc = {
                    'labels': ['Cuenta'],
                    'key_property': 'no_cuenta',
                    'key_value': account_no
                }

                remove_relationship_property(session, node_info, node_info_acc, 'fraudulenta', 'TITULAR')

    except Exception as e:
        raise RuntimeError(f'Failed to remove fraud')
    finally:
        close_driver()


def edit_fraude_in_titulacion(dpi_or_nit, is_fraud: bool, is_dpi: bool = True):
    try:
        driver = get_driver()
        with driver.session() as session:

            accounts = get_user_accounts(session, dpi_or_nit, is_dpi=is_dpi)

            if is_dpi:
                node_info = {
                    'labels': ['Individuo'],
                    'key_property': 'dpi',
                    'key_value': dpi_or_nit
                }
            else:
                node_info = {
                    'labels': ['Empresa'],
                    'key_property': 'nit',
                    'key_value': dpi_or_nit
                }

            for account_no in accounts:
                node_info_acc = {
                    'labels': ['Cuenta'],
                    'key_property': 'no_cuenta',
                    'key_value': account_no
                }

                properties = {
                    'fraudulenta': is_fraud
                }

                update_relationship(session, node_info, node_info_acc, 'TITULAR', properties)

    except Exception as e:
        raise RuntimeError(f'Failed to edit fraud in titulacion: {e}')
    finally:
        close_driver()


def display_trans_history_(account_no):
    try:
        driver = get_driver()
        with driver.session() as session:
            transaction_history(session, account_no)

            node_info = {
                'labels': ['Cuenta'],
                'key_property': 'no_cuenta',
                'key_value': account_no
            }
            display_trans_history(session, node_info)

    except Exception as e:
        raise RuntimeError(f'Failed to display transaction history: {e}')
    finally:
        close_driver()
