from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./TODO_TASK.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:997480@localhost:5434/TodoApplicationDataBase"  # pip install psycopg2-binary
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:A1b2c3d47**@127.0.0.1:3306/todo_app"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()
