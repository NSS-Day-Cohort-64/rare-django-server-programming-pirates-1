from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from piratesrareapi.models import Post, Author, Category
from datetime import datetime

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
        posts = Post.objects.order_by('-publication_date')
        if "user" in request.query_params:
            author = Author.objects.get(user=request.auth.user)
            posts = posts.filter(author=author)
        
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized post instance
        """
        new_post = Post()
        new_post.category = Category.objects.get(pk=request.data["category_id"])
        author = Author.objects.get(user = request.auth.user)
        new_post.author = author
        new_post.title = request.data["title"]
        new_post.publication_date = datetime.now()
        new_post.image_url = request.data["image_url"]
        new_post.content = request.data["content"]
        new_post.approved = True

        new_post.save()

        serializer = PostSerializer(new_post, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a post
        Returns:
            Response -- Empty body with 204 status code
        """
        post = Post.objects.get(pk=pk)
        category = Category.objects.get(pk=request.data["category_id"])
        post.category = category
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self,_, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status= status.HTTP_204_NO_CONTENT)

class PostAuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for post author
    Arguments:
        serializer type
    """
    class Meta:
        model = Author
        fields = ('full_name',)
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    Arguments:
        serializer type
    """
    author = PostAuthorSerializer(many=False)
    class Meta:
        model = Post
        fields = ('id', 'author', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved')
        depth = 1
