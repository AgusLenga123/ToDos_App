# The modeling of the DataBase:

from database import Base
from sqlalchemy import Column, Integer, String, Boolean

# This model inherits the database config done in the database.py file
class Todos(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
