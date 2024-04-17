from controller.db_connection import *
from controller.db_crud import *

try:
    driver = get_driver()


except Exception as e:
    print(f"ERROR: {e}")

finally:
    close_driver()