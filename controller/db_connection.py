import os
import dotenv
from neo4j import GraphDatabase

def load_credentials(filepath='.env'):
    load_status = dotenv.load_dotenv(filepath)
    
    if not load_status:
        raise RuntimeError('ERROR: Failed to load credentials from .env file')
    
    URI = os.getenv('NEO4J_URI')
    AUTH = (os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD'))

    if not URI or not AUTH:
        raise RuntimeError('ERROR: Missing credentials in .env file')
    
    return URI, AUTH


def get_driver():
    URI, AUTH = load_credentials()
    try:
        driver = GraphDatabase.driver(uri=URI, auth=AUTH)
        driver.verify_connectivity()
        print('INFO: Successfully connected to Neo4j database')
        return driver
    
    except Exception as e:
        raise RuntimeError(f'ERROR: Failed to connect to Neo4j database: {e}')

    # En controlador hay que asegurarse de hacer driver.close() al finalizar la conexión
    # Usar with driver.session() as session: para asegurar que se cierre la sesión
    # Encapsular el código de la conexión en un try-except para manejar errores