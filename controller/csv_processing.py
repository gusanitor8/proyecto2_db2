import pandas as pd
from db_crud import create_node


def process_csv_nodes(csv_filepath, session):
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
                        key_value = value

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