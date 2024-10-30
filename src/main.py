from fastapi import FastAPI

from .database import nuke_database, push_model_updates
from .routers import auth, post, user, vote

app = FastAPI()


# update mode
# nuke_database()
push_model_updates()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return "meme project"
