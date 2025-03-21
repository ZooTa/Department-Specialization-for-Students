from database_config import engine
from base_models import Base
import models

def init_db():
    Base.metadata.create_all(engine)
    print("Database and tables created successfully.")
