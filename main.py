from controller.controller import run
from controller.db_connection import *
try:
    driver = get_driver()
    with driver.session() as session:
        run(session)

except Exception as e:
    print(f"ERROR: {e}")

finally:
    driver.close()