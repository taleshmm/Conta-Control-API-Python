import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import accounts
import auth
import permissions
import users

app = FastAPI()
app.add_middleware(CORSMiddleware, 
                   allow_origins=["https://ekros.com.br"], 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"])

app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users"])
app.include_router(permissions.router, tags=["Permissions"])
app.include_router(accounts.router, tags=["Account"])

if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000) 
