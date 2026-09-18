from fastapi.middleware.cors import CORSMiddleware
from .routers import posts, users, auth, vote
from fastapi import FastAPI, status
from .database import engine
from . import models

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

"""
    root 
"""

# ROOT URL
@app.get("/",status_code=status.HTTP_200_OK)
async def root():

    return {"message":"this is the root"}


