'''
GraphQL is an alternative to REST developed by Facebook. It allows clients to request exactly the data they need and nothing more. In GraphQL, you define queries to specify which fields of data you want, avoiding the over-fetching or under-fetching common with REST APIs.

Setting Up a GraphQL API in Django:
'''

# Install Django Graphene: Graphene is a library used to build GraphQL APIs in Django.

pip install graphene-django

# Configure GraphQL in Django: In settings.py, add 'graphene_django' to INSTALLED_APPS.

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # other apps
    'graphene_django',
]

GRAPHENE = {
    'SCHEMA': 'myapp.schema.schema'
}

# Create GraphQL Schema: Define the schema for querying and mutating your models.

import graphene
from graphene_django.types import DjangoObjectType
from .models import Branch, Sale

class BranchType(DjangoObjectType):
    class Meta:
        model = Branch

class SaleType(DjangoObjectType):
    class Meta:
        model = Sale

class Query(graphene.ObjectType):
    branches = graphene.List(BranchType)
    sales = graphene.List(SaleType)

    def resolve_branches(self, info):
        return Branch.objects.all()

    def resolve_sales(self, info):
        return Sale.objects.all()

class CreateBranch(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        location = graphene.String()
        manager_id = graphene.Int()

    branch = graphene.Field(BranchType)

    def mutate(self, info, name, location, manager_id):
        manager = User.objects.get(id=manager_id)
        branch = Branch(name=name, location=location, manager=manager)
        branch.save()
        return CreateBranch(branch=branch)

class Mutation(graphene.ObjectType):
    create_branch = CreateBranch.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# Add URL for GraphQL: In urls.py, add a route for GraphQL.

from django.urls import path
from graphene_django.views import GraphQLView

urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True)),  # GraphiQL is a GraphQL interface
]


# Using the GraphQL API: You can query and mutate data using GraphQL. For example:
# Query
{
  branches {
    id
    name
    location
    manager {
      id
      username
    }
  }
}

# Mutate
mutation {
  createBranch(name: "Branch A", location: "Downtown", managerId: 1) {
    branch {
      id
      name
    }
  }
}

'''
Pros of GraphQL:
Flexibility: Clients can specify exactly what data they need.
Efficiency: Reduces the number of requests (fetch multiple resources in one call).
Strongly typed: Clear schema definitions make the API predictable.

When to Choose REST vs. GraphQL
REST:

Suitable for simple, resource-based APIs.
Use if your API clients only need specific endpoints.
Well-supported by browsers and many tools.
GraphQL:

Ideal for complex, interrelated data where clients may request varying levels of detail.
Use if the frontend requires flexibility in requesting different fields of data.
Reduces the number of API calls for highly relational data structures.

Pros of GraphQL:
Flexibility: Clients can specify exactly what data they need.
Efficiency: Reduces the number of requests (fetch multiple resources in one call).
Strongly typed: Clear schema definitions make the API predictable.
When to Choose REST vs. GraphQL
REST:

Suitable for simple, resource-based APIs.
Use if your API clients only need specific endpoints.
Well-supported by browsers and many tools.
GraphQL:

Ideal for complex, interrelated data where clients may request varying levels of detail.
Use if the frontend requires flexibility in requesting different fields of data.
Reduces the number of API calls for highly relational data structures.
Conclusion
REST: Great for standard CRUD operations with simple endpoints.
GraphQL: Ideal when you need flexibility and efficiency in querying and mutating complex, nested data.
For your gas station management app, REST might be simpler to start with, especially for standard CRUD operations, while GraphQL would shine if you expect complex queries with relationships (e.g., fetching branch data along with sales records in one request).
'''
