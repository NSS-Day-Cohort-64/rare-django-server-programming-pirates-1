from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class TokenView(ViewSet):
    def list(self, request):
        """Handle GET requests to tokens resource
        Returns:
            Response -- JSON serialized list of tokens
        """
        tokens = Token.objects.all()
        serializer = TokenSerializer(tokens, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single token
        Returns:
            Response -- JSON serialized token instance
        """
        token = Token.objects.get(pk=pk)
        serializer = TokenSerializer(token)
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined')

class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Token
        fields = ('key', 'user')
