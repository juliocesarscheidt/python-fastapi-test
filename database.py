import os
import databases
from sqlalchemy import create_engine
from notes_model import metadata
from log import logger

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./test.db')

database = databases.Database(DATABASE_URL)
logger.info('Creating database')

engine = create_engine(DATABASE_URL, echo=True, future=True,
                      connect_args={'check_same_thread': False})
metadata.create_all(engine)

def inject_database():
  logger.info('Retrieving database')
  return database
