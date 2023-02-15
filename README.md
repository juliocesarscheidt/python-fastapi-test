
```bash

python main.py

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2


curl --silent -X POST \
  -H 'Content-type: application/json' \
  --data '{"description": "Hello World", "completed": false}' \
  --url 'http://127.0.0.1:8000/v1/notes'

curl -X GET --url 'http://127.0.0.1:8000/v1/notes'

curl --silent -X PUT \
  -H 'Content-type: application/json' \
  --data '{"description": "Hello World 2", "completed": true}' \
  --url 'http://127.0.0.1:8000/v1/notes/1'


# swagger
http://127.0.0.1:8000/docs#/
http://127.0.0.1:8000/openapi.json

```
