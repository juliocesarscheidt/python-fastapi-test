from fastapi import APIRouter, BackgroundTasks, Depends
from log import logger
from worker import append_log_bg
from http_response_dto import HttpResponseDto
from notes_dto import CreateNoteDto, UpdateNoteDto
from database import inject_database
from notes_repository import inject_notes_repository

notes_router = APIRouter()

# routes
@notes_router.post('', response_model=HttpResponseDto)
async def create_note(create_note_dto: CreateNoteDto, background_tasks: BackgroundTasks, database=Depends(inject_database), notes_repository=Depends(inject_notes_repository)):
  logger.info(create_note_dto)
  background_tasks.add_task(append_log_bg, str(create_note_dto))
  response = await notes_repository(database).create_note(create_note_dto)
  logger.info(response)
  return HttpResponseDto(
    data=response,
    metadata=None
  )

@notes_router.get('', response_model=HttpResponseDto)
async def list_notes(_: BackgroundTasks, database=Depends(inject_database), notes_repository=Depends(inject_notes_repository)):
  response = await notes_repository(database).list_notes()
  logger.info(response)
  return HttpResponseDto(
    data=response,
    metadata=None
  )

@notes_router.put('/{id}', response_model=HttpResponseDto)
async def update_item(id: int, update_note_dto: UpdateNoteDto, background_tasks: BackgroundTasks, database=Depends(inject_database), notes_repository=Depends(inject_notes_repository)):
  logger.info(update_note_dto)
  background_tasks.add_task(append_log_bg, str(update_note_dto))
  await notes_repository(database).update_note(id, update_note_dto)
  return HttpResponseDto(
    status='Accepted',
    data=None,
    metadata=None
  )
