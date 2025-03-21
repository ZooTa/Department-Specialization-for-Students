from sqlalchemy import create_engine

DATABASE_URI = 'sqlite:///database.db'
engine = create_engine(DATABASE_URI)
