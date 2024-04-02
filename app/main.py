from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from pydantic_core._pydantic_core import ValidationError





# this is to create a new all db table anytime your run the app or check if it's created before creating it.
# now that we have alembic we do not need it cos it does same and more
# models.Base.metadata.create_all(bind=engine)


# providing the list of domaims that can use your api
# origins = ['https://www.google.com']
# every domain can access it
origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "welcome to my api!!!"}
