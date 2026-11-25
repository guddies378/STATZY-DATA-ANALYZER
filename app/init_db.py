from app.database.connection import engine, Base
from app import models

def initialize_database():
    Base.metadata.create_all(bind=engine)
    print("STATZY database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
