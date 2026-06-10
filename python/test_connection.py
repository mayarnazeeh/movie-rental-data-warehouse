import pandas as pd
from sqlalchemy import create_engine
import pymysql
import mysql.connector
from sqlalchemy.engine import URL

USER = "root"
PASSWORD = "your_mysql_password"
HOST = "127.0.0.1"
PORT = 3306

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

engine = create_engine(connection_url)

try:
    with engine.connect() as connection:
        print("Connected to MySQL successfully!")
except Exception as e:
    print("Connection failed!")
    print(e)