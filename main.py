from typing import List

import threading
import queue
import databases
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, create_engine
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DATABASE_URL = 'sqlite:///./test.db'
database = databases.Database(DATABASE_URL)
metadata = MetaData()

# defining entities
notes = Table(
  'notes',
  metadata,
  Column('id', Integer, primary_key=True),
  Column('description', String(255)),
  Column('completed', Boolean),
)

engine = create_engine(DATABASE_URL, echo=True,
                      future=True, connect_args={'check_same_thread': False})
metadata.create_all(engine)

# create a queue to handle background tasks
q = queue.Queue()

def worker():
  while True:
    message = q.get()
    print(f'Working on {message}')
    with open('log.txt', mode='a') as f:
      f.write(message + '\n')
    print(f'Finished {message}')
    q.task_done()

def write_log(message: str):
  q.put(message)

# dtos
class CreateNoteDto(BaseModel):
  description: str
  completed: bool

class UpdateNoteDto(BaseModel):
  description: str
  completed: bool

class NoteDto(BaseModel):
  id: int
  description: str
  completed: bool

# API
app = FastAPI()
origins = [
  'http://localhost',
  'http://localhost:8000',
]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

# events
@app.on_event('startup')
async def startup():
  print('startup')
  await database.connect()

@app.on_event('shutdown')
async def shutdown():
  print('shutdown')
  await database.disconnect()

# routes
@app.post('/v1/notes', response_model=NoteDto)
async def create_note(create_note_dto: CreateNoteDto, background_tasks: BackgroundTasks):
  print('create_note_dto', create_note_dto)
  background_tasks.add_task(write_log, str(create_note_dto))

  query = notes.insert().values(
    description=create_note_dto.description,
    completed=create_note_dto.completed
  )
  last_record_id = await database.execute(query)
  print('last_record_id', last_record_id)

  response_dto = NoteDto(
    id = last_record_id,
    description = create_note_dto.description,
    completed = create_note_dto.completed
  )
  print('response_dto', response_dto)
  return response_dto

@app.get('/v1/notes', response_model=List[NoteDto])
async def list_notes(background_tasks: BackgroundTasks):
  query = notes.select()
  response_dto = await database.fetch_all(query)
  print('response_dto', response_dto)

  return response_dto

@app.put('/v1/notes/{id}', response_model=NoteDto)
async def update_item(id: int, update_note_dto: UpdateNoteDto, background_tasks: BackgroundTasks):
  print('update_note_dto', update_note_dto)
  background_tasks.add_task(write_log, str(update_note_dto))

  query = notes.update().where(notes.c.id==id).values(
    description=update_note_dto.description,
    completed=update_note_dto.completed
  )
  await database.execute(query)

  response_dto = NoteDto(
    id = id,
    description = update_note_dto.description,
    completed = update_note_dto.completed
  )
  print('response_dto', response_dto)
  return response_dto

# turns-on the worker thread
threading.Thread(target=worker, daemon=True).start()
# blocks until all items in the queue have been processed
q.join()
