import pandas as pd
from db_crud import *


def process_csv_nodes(csv_filepath, session):
    """
    Process a CSV file containing node data and create nodes in the database.

    Args:
        csv_filepath (str): The file path of the CSV file.
        session: The session object for interacting with the database.

    Raises:
        ValueError: If the CSV format is not valid or the row data is invalid.

    Returns:
        None
    """

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filepath)

    # Required columns for the CSV file
    required_columns = [
        'nombre_empresa', 'nit_empresa', 'direccion_empresa', 'regimen_empresa',
        'sector_empresa', 'telefono_empresa', 'email_empresa', 'representante_legal_empresa',
        'fecha_creacion_empresa', 'nombre_individuo', 'edad_individuo', 'dpi_individuo',
        'nit_individuo', 'direccion_individuo', 'telefono_individuo', 'email_individuo',
        'no_cuenta_cuenta', 'saldo_cuenta', 'fecha_apertura_cuenta', 'divisa_cuenta',
        'estado_cuenta', 'limite_retiro_monetaria', 'tasa_interes_ahorro', 'limite_retiro_ahorro',
        'objetivo_ahorro', 'vencimiento_plazo', 'capital_inicial_plazo', 'frecuencia_pago_plazo',
        'tasa_interes_plazo'
    ]

    # Validate the format of the CSV file
    if not all(column in df.columns for column in required_columns):
        raise ValueError("CSV format not valid: missing required columns")


    # Loop through the rows of the DataFrame
    for index, row in df.iterrows():
        labels = set()
        properties = {}
        key_property = None
        key_value = None

        # Identify the labels and properties based on the column suffix
        for col in df.columns:
            value = row[col]
            if pd.notna(value):  # Check if the value is not Null
                if '_empresa' in col:
                    labels.add('Empresa')
                    property_name = col.replace('_empresa', '')
                    if property_name == 'nit':
                        key_property = 'nit'
                        key_valccue = value
                    properties[property_name] = value

                elif '_individuo' in col:
                    labels.add('Individuo')
                    property_name = col.replace('_individuo', '')
                    if property_name == 'dpi':
                        key_property = 'dpi'
                        key_value = value
                    properties[property_name] = value

                elif '_cuenta' in col:
                    labels.add('Cuenta')
                    property_name = col.rsplit('_cuenta', 1)[0]  # This will only replace the last '_cuenta'
                    if property_name == 'no_cuenta':
                        key_property = 'no_cuenta'
                        key_value = value
                    properties[property_name] = value

                elif '_monetaria' in col:
                    labels.add('Monetaria')
                    property_name = col.replace('_monetaria', '')
                    properties[property_name] = value

                elif '_ahorro' in col:
                    labels.add('Ahorro')
                    property_name = col.replace('_ahorro', '')
                    properties[property_name] = value

                elif '_plazo' in col:
                    labels.add('Plazo')
                    property_name = col.replace('_plazo', '')
                    properties[property_name] = value

        # create the node if labels and properties and key_property
        if labels and properties and key_property:
            node_info = {
                'labels': list(labels),
                'properties': properties,
                'key_property': key_property,
                'key_value': key_value
            }
            print(create_node(session, node_info))
        else:
            raise ValueError("Invalid row data. Please check the CSV file.")
        

def process_csv_relationships(csv_filepath, session):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filepath)

    # Required columns for the CSV file
    required_columns = [
       'dpi_titular', 'nit_titular', 'no_cuenta_titular', 'fecha_inicio_titular', 
       'rol_titular', 'estado_titular', 'cuenta_origen_tran', 'cuenta_destino_tran', 
       'fecha_tran', 'descripcion_tran', 'ubicacion_tran', 'tipo_tran', 'alerta_tran', 
       'monto_tran'
    ]

    # Validate the format of the CSV file
    if not set(required_columns).issubset(df.columns):
        missing_columns = set(required_columns) - set(df.columns)
        raise ValueError(f"CSV format not valid: missing required columns {missing_columns}")
    
    # Loop through the rows of the DataFrame
    for index, row in df.iterrows():
        # Variables to store node and relationship information
        node1_info = {}
        node2_info = {}
        relationship_properties = {}

        # Mapping the columns to the corresponding nodes and relationships
        if pd.notna(row['dpi_titular']):
            node1_info = {
                'labels': ['Individuo'],
                'key_property': 'dpi',
                'key_value': row['dpi_titular']
            }
        elif pd.notna(row['nit_titular']):
            node1_info = {
                'labels': ['Empresa'],
                'key_property': 'nit',
                'key_value': row['nit_titular']
            }


        if pd.notna(row['no_cuenta_titular']):
            node2_info = {
                'labels': ['Cuenta'],
                'key_property': 'no_cuenta',
                'key_value': row['no_cuenta_titular']
            }

        # Create relationship properties
        if pd.notna(row['fecha_inicio_titular']):
            relationship_properties['fecha_inicio'] = row['fecha_inicio_titular']
        if pd.notna(row['rol_titular']):
            relationship_properties['rol'] = row['rol_titular']
        if pd.notna(row['estado_titular']):
            relationship_properties['estado'] = row['estado_titular']

        # Create relationship if node information is available
        if node1_info and node2_info:
            create_relationship(session, node1_info, node2_info, 'TITULAR', relationship_properties)

        # Clear node and relationship information
        node1_info = {}
        node2_info = {}
        relationship_properties = {}

        # Mapping the columns to the corresponding nodes and relationships
        if pd.notna(row['cuenta_origen_tran']) and pd.notna(row['cuenta_destino_trans']):
            node1_info = {
                'labels': ['Cuenta'],
                'key_property': 'no_cuenta',
                'key_value': row['cuenta_origen_tran']
            }
            node2_info = {
                'labels': ['Cuenta'],
                'key_property': 'no_cuenta',
                'key_value': row['cuenta_destino_tran']
            }

            # Add relationship properties
            if pd.notna(row['fecha_tran']):
                relationship_properties['fecha'] = row['fecha_tran']
            if pd.notna(row['descripcion_tran']):
                relationship_properties['descripcion'] = row['descripcion_tran']
            if pd.notna(row['ubicacion_tran']):
                relationship_properties['ubicacion'] = row['ubicacion_tran']
            if pd.notna(row['tipo_tran']):
                relationship_properties['tipo'] = row['tipo_tran']
            if pd.notna(row['alerta_trans']):
                relationship_properties['alerta'] = row['alerta_tran']
            if pd.notna(row['monto_tran']):
                relationship_properties['monto'] = row['monto_tran']

            # create relationship if node information is available
            if node1_info and node2_info:
                create_relationship(session, node1_info, node2_info, 'TRANSACCION', relationship_properties)