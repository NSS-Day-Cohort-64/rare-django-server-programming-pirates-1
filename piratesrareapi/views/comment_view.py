from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from piratesrareapi.models import Comment, Post, Author

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
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized comment instance
        """
        new_comment = Comment()
        new_comment.author = Author.objects.get(pk=request.data["author_id"])
        new_comment.post = Post.objects.get(pk=request.data["post"])
        new_comment.author = request.data["author"]
        new_comment.content = request.data["content"]

        new_comment.save()

        serializer = CommentSerializer(new_comment, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a comment
        Returns:
            Response -- Empty body with 204 status code
        """
        comment = Comment.objects.get(pk=pk)
        author = Author.objects.get(pk=request.data["author_id"])
        comment.author = author
        post = Post.objects.get(pk=request.data["post"])
        comment.content = request.data["content"]

        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments
    Arguments:
        serializer type
    """
    class Meta:
        model = Comment
        fields = ('id', 'user', 'author', 'post', 'content')