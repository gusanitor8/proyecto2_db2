from controller.db_connection import *
from controller.csv_processing import *

try:

    driver = get_driver(path='.env')
    with driver.session() as session:
        process_csv_nodes('utils/nodes.csv', session)
        process_csv_relationships('utils/relations.csv', session)

except Exception as e:
    print(f"ERROR: {e}")

finally:
    close_driver()