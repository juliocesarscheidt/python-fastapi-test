import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import inject_database
from notes_repository import inject_notes_repository
from notes_controller import notes_router

# API
app = FastAPI()

origins = [
  'http://localhost:8000',
]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

app.include_router(
  notes_router,
  prefix='/v1/notes',
  tags=['notes'],
  dependencies=[Depends(inject_database), Depends(inject_notes_repository)],
  responses={404: {'message': 'Not found'}},
)

if __name__ == '__main__':
  uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, access_log=True)
