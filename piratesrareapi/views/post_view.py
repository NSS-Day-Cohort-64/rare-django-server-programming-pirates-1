from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from piratesrareapi.models import Post, Author, Category

class PostView(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for single post
        Returns:
            Response -- JSON serialized post instance
        """
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to posts resource
        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized post instance
        """
        new_post = Post()
        new_post.category = Category.objects.get(pk=request.data["category"])
        new_post.title = request.data["title"]
        new_post.publication_date = request.data["publication_date"]
        new_post.image_url = request.data["image_url"]
        new_post.content = request.data["content"]
        new_post.approved = request.data["approved"]

        new_post.save()

        serializer = PostSerializer(new_post, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a post
        Returns:
            Response -- Empty body with 204 status code
        """
        post = Post.objects.get(pk=pk)
        category = Category.objects.get(pk=request.data["category"])
        post.category = category
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, pk):
        post = Post.objects.get(pk = pk)
        post.delete()
        return Response({}, status= status.HTTP_204_NO_CONTENT)
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    Arguments:
        serializer type
    """
    class Meta:
        model = Post
        fields = ('id', 'author', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved')
        depth = 1