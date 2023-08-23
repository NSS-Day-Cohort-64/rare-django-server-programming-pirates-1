from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import datetime
from piratesrareapi.models import Author

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Handles the authentication of a user
    
    Method arguments:
        request -- The full HTTP request object
    """

    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = { 'valid': True, 'token': token.key }
        return Response(data)
    else:
        data = { 'valid': False }
        return Response(data)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Handles the creation of a new user for authentication
    
    Method arguments:
        request -- The full HTTP request object
    """

    new_user = User.objects.create_user(
        username=request.data['username'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=request.data['email'],
        password=request.data['password'],
    )

    author = Author.objects.create(
        created_on=datetime.now(),
        active=True,
        user = new_user
    )


    token = Token.objects.create(user=author.user)
    data = { 'token': token.key }
    return Response(data)
