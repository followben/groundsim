import strawberry
from api.graphql.queries import Query, Subscription

schema = strawberry.Schema(query=Query, subscription=Subscription)
