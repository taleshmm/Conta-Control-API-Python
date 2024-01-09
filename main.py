import uvicorn
from fastapi import FastAPI
import permissions
import users

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(permissions.router, prefix="/permissions", tags=["permissions"])

if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000) 
""" if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000) 
  colocar no lauch.json
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "cwd": "${workspaceFolder}/",
      "args": ["main:app", "--reload", "--port", "8000"],
      "jinja": true,
      "justMyCode": true
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
  """
