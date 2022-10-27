from api.graphql.schema import schema
from strawberry.fastapi import GraphQLRouter

graphql_router = GraphQLRouter(schema)
