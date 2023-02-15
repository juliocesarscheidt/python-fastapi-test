
from typing import Any, List
from log import logger
from notes_model import notes
from notes_dto import CreateNoteDto, UpdateNoteDto, NoteDto

class NotesRepository():
  database: Any

  def __init__(self, database) -> None:
    self.database = database

  async def list_notes(self) -> List[NoteDto]:
    query = notes.select()
    response = await self.database.fetch_all(query)
    logger.info(response)
    return list([NoteDto(id=note['id'], description=note['description'], completed=note['completed']) for note in response])

  async def create_note(self, create_note_dto: CreateNoteDto) -> int:
    query = notes.insert().values(
      description=create_note_dto.description,
      completed=create_note_dto.completed
    )
    response = await self.database.execute(query)
    logger.info(response)
    return response

  async def update_note(self, _id: int, update_note_dto: UpdateNoteDto) -> None:
    query = notes.update().where(notes.c.id==_id).values(
      description=update_note_dto.description,
      completed=update_note_dto.completed
    )
    await self.database.execute(query)

def inject_notes_repository():
  def get(database):
    return NotesRepository(database)
  return get
