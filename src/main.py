from fastapi import FastAPI
from .routers import post, user, auth
from .database import nuke_database, push_model_updates

app = FastAPI()


# update mode
# nuke_database()
# push_model_updates()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return "meme project"
