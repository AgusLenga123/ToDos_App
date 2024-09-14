from sqlalchemy import create_engine # conection to database
from sqlalchemy.orm import sessionmaker # new session objects that manage db
from sqlalchemy.ext.declarative import declarative_base # constructs a base class 

# Directory for database
SQLALCHEMY_DATAABASE_URL = "sqlite:///./todos.db"

# Creating the database:
engine = create_engine(SQLALCHEMY_DATAABASE_URL, connect_args={"check_same_thread": False}) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()