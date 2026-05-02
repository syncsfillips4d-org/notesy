"""GraphQL — read-only views over notes."""
import strawberry
from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Note:
    id: strawberry.ID
    title: str
    body: str
    author: str


@strawberry.type
class Query:
    @strawberry.field
    def notes(self) -> list[Note]:
        from app.routers.notes_api import _notes  # avoid circular import

        return [Note(id=strawberry.ID(str(n.id)), title=n.title, body=n.body, author=n.author) for n in _notes]


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

router = APIRouter()
router.include_router(graphql_app, prefix="/graphql")
