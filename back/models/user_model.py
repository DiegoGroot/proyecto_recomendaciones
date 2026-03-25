from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users" # poner el nombre de la tabla

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)