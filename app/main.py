from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .routers import merchants, transactions, users, auth
from . import models

models.Base.metadata.create_all(bind=engine)

app =FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],            # defines allowed methods like PUT, POST
    allow_headers=["*"],            # defines list of headers alloweded by API
)

app.include_router(users.router)
app.include_router(merchants.router)
app.include_router(transactions.router)
app.include_router(auth.router)