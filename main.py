from fastapi import FastAPI
from typing import List
from strawberry.asgi import GraphQL
from schema import schema

import database

app = FastAPI()

app.mount("/graphql",  GraphQL(schema, debug=True))

@app.get("/")
async def root():
    return {
        "ping": "pong"
    }