from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:Hola123@localhost:3306/todoApp"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
except OperationalError as e:
    print(f"Error al conectar a la base de datos: {e}")

Base = declarative_base()
