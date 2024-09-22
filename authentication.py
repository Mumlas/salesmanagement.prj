''' Implementing JWT Authentication in Django: '''

# 1. For a RESTful API:

# Step 1: Install djangorestframework-simplejwt -This library integrates JWT with Django REST Framework
pip install djangorestframework-simplejwt

# Step 2: Update settings.py - Add the JWT authentication to your Django REST Framework settings.
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    # other apps
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Step 3: Create Login View for Token Generation - Create a login view using Simple JWT for obtaining the access token and refresh token.
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Step 4: Protect API Endpoints - Use Django REST Framework’s permission classes to protect views based on the user’s authentication.
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Branch
from .serializers import BranchSerializer

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

# Step 5: Usage
'''
Login (Token Generation): POST request to /api/token/ with username and password to receive an access token and refresh token.

Access API: Attach the token to the Authorization header of your API requests: '''
GET /api/branches/
Authorization: Bearer <your_access_token>

# 2. For GraphQL API:

# Step 1: Install GraphQL JWT Library -Graphene JWT provides JWT authentication for GraphQL APIs.
pip install django-graphql-jwt

# Step 2: Configure settings.py - Add graphql_jwt to your INSTALLED_APPS and configure the GraphQL schema to use JWT authentication.
INSTALLED_APPS = [
    'graphene_django',
    'graphql_jwt',
]

GRAPHENE = {
    'SCHEMA': 'myapp.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Step 3: Add Login Mutation - Add JWT authentication mutations (e.g., token authentication) to your GraphQL schema.
import graphene
import graphql_jwt

class Query(graphene.ObjectType):
    # Your existing queries
    pass

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# Step 4: Protect GraphQL Queries/Mutations -vUse the @login_required decorator or IsAuthenticated permission for protecting specific queries and mutations.
from graphene_django.types import DjangoObjectType
from .models import Branch
from graphql_jwt.decorators import login_required

class BranchType(DjangoObjectType):
    class Meta:
        model = Branch

class Query(graphene.ObjectType):
    branches = graphene.List(BranchType)

    @login_required
    def resolve_branches(self, info):
        return Branch.objects.all()

# Step 5: Usage - Login (Token Generation):
mutation {
  tokenAuth(username: "your_username", password: "your_password") {
    token
  }
}

# Access Protected Queries: Attach the JWT token to the Authorization header in your GraphQL requests
POST /graphql/
Authorization: JWT <your_token>

