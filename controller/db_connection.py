import os
import dotenv
from neo4j import GraphDatabase

# Global variable for Neo4j driver
neo4j_driver = None

def load_credentials(filepath='.env'):
    """
    Load the credentials from a .env file.

    Args:
        filepath (str): The path to the .env file. Default is '.env'.

    Returns:
        tuple: A tuple containing the URI and authentication credentials.

    Raises:
        RuntimeError: If the .env file fails to load or if the credentials are missing.
    """
    load_status = dotenv.load_dotenv(filepath)
    if not load_status:
        raise RuntimeError('ERROR: Failed to load credentials from .env file')

    URI = os.getenv('NEO4J_URI')
    AUTH = (os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD'))

    if not URI or not AUTH:
        raise RuntimeError('ERROR: Missing credentials in .env file')
    
    return URI, AUTH


def init_driver():
    """
    Initializes and returns a Neo4j driver instance.

    This function checks if a driver instance already exists. If not, it loads the credentials,
    establishes a connection to the Neo4j database, and verifies the connectivity. If any error
    occurs during the connection process, a RuntimeError is raised.

    Returns:
        The Neo4j driver instance.

    Raises:
        RuntimeError: If failed to connect to the Neo4j database.
    """
    global neo4j_driver
    if neo4j_driver is None:
        URI, AUTH = load_credentials()
        try:
            neo4j_driver = GraphDatabase.driver(URI, auth=AUTH)
            neo4j_driver.verify_connectivity()
            print('INFO: Successfully connected to Neo4j database')
        except Exception as e:
            raise RuntimeError(f'ERROR: Failed to connect to Neo4j database: {e}')

    return neo4j_driver


def get_driver():
    """
    Retrieves the Neo4j driver instance.

    If the driver instance is not initialized, it will be initialized by calling the `init_driver` function.

    Returns:
        The Neo4j driver instance.
    """
    if neo4j_driver is None:
        return init_driver()
    return neo4j_driver


def close_driver():
    """
    Closes the Neo4j driver if it is not None.

    This function closes the Neo4j driver connection if it is not None. It also sets the global variable `neo4j_driver` to None.

    Returns:
        None
    """
    global neo4j_driver
    if neo4j_driver is not None:
        neo4j_driver.close()
        print('INFO: Neo4j driver closed')
        neo4j_driver = None


# MODO DE USO
# try:
#         # Initialize and get the driver
#         driver = get_driver()
#
#         # Perform database operations here
#         with driver.session() as session:
#             result = session.run('MATCH (n) RETURN count(n) AS count')
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#     finally:
#         # Ensure the driver is closed properly
#         close_driver()