
from fastapi import FastAPI

import users

app = FastAPI()

app.include_router(users.router)


