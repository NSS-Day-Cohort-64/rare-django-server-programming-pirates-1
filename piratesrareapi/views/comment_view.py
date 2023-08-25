from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from piratesrareapi.models import Comment, Post, Author
from datetime import datetime

class CommentView(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment
        Returns:
            Response -- JSON serialized comment instance
        """
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to comments resource
        Returns:
            Response -- JSON serialized list of comments
        """
        # Get the value of the 'post' query parameter from the request
        post_id = self.request.query_params.get('post')

        # Filter comments based on the provided 'post' query parameter
        if post_id:
            comments = Comment.objects.filter(post=post_id)
        else:
            comments = Comment.objects.all()

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized comment instance
        """
        new_comment = Comment()
        author = Author.objects.get(user = request.auth.user)
        new_comment.author = author
        new_comment.post = Post.objects.get(pk=request.data["post"])
        new_comment.content = request.data["content"]

        new_comment.save()

        serializer = CommentSerializer(new_comment, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a comment
        Returns:
            Response -- Empty body with 204 status code
        """
        comment = Comment.objects.get(pk=pk)
        post = Post.objects.get(pk=request.data["post"])
        comment.post = post
        comment.content = request.data["content"]

        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self,_, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status= status.HTTP_204_NO_CONTENT)


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments
    Arguments:
        serializer type
    """
    created_at = serializers.DateTimeField(default=datetime.now, read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content', 'created_at')
