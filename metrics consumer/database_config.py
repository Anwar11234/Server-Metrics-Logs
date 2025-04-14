import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
dbname = 'metrics'
DATABASE_URL = f"postgresql://{username}:{password}@localhost/{dbname}"
engine = create_engine(DATABASE_URL)

Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)