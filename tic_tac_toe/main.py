from fastapi import FastAPI

from routers import game_field, user_auth

app = FastAPI()

app.include_router(router=user_auth.router)
app.include_router(router=game_field.router)
