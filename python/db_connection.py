from sqlalchemy import create_engine
from sqlalchemy.engine import URL

USER = "root"
PASSWORD = "your_mysql_password"
HOST = "127.0.0.1"
PORT = 3306

SOURCE_DB = "movie_rental_source"
DW_DB = "movie_rental_dw"

source_url = URL.create(
    drivername="mysql+pymysql",
    username=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database=SOURCE_DB
)

dw_url = URL.create(
    drivername="mysql+pymysql",
    username=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database=DW_DB
)

source_engine = create_engine(source_url)
dw_engine = create_engine(dw_url)