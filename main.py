from routers import todo, token, user
from fastapi import FastAPI
from config.database import register


app = FastAPI(title='Todolist App')
app.include_router(token.router)
app.include_router(user.router)
app.include_router(todo.router)
register(app)
