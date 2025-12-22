from dotenv import load_dotenv
import os 
import sys

load_dotenv()

class DatabaseConfig:
    
    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")
        
        if not all([self.DB_HOST, self.DB_PORT, self.DB_USER, self.DB_PASSWORD, self.DB_NAME]):
            print("database variables were not set properly in .env file.")
            sys.exit(1)
            
        self.ENVIRONMENT = os.getenv('ENVIRONMENT')
        self.DEBUG = os.getenv('DEBUG') == 'True'
        
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def __repr__(self):
        return f"<DatabaseConfig(environment={self.ENVIRONMENT}, database={self.DB_NAME})>"

config = DatabaseConfig()
        