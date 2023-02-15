from pydantic import BaseModel

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
