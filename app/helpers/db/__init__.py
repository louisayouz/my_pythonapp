import os

db_type = os.getenv("DB_SUPPORT", "postgres")  # default to postgres

if db_type == "mysql":
    from .db_mysql import *
else:
    from .db_postgres import *