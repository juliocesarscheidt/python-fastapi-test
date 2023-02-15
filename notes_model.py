from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean
metadata = MetaData()

notes = Table(
  'notes',
  metadata,
  Column('id', Integer, primary_key=True),
  Column('description', String(255)),
  Column('completed', Boolean),
)
