from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.graphql.schema import schema
from app.graphql.context import get_context

import app.infrastructure.models
app = FastAPI(
    title="Volunthub Backend v2.0",
    summary="Migracion del backend de Volunthub desde express a fastapi con base de datos local postgres",
)

graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"messagle": "Hello World"}
