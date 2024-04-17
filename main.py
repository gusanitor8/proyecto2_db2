from controller.db_connection import *
from controller.db_crud import *
from controller.controller import *


try:
    driver = get_driver()
    with driver.session() as session:
        run(session)

except Exception as e:
    print(f"ERROR: {e}")

finally:
    driver.close()