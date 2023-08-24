from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from piratesrareapi.models import Tag

class TagView(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag
        Returns:
            Response -- JSON serialized tag instance
        """
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to tags resource
        Returns:
            Response -- JSON serialized list of tags
        """
        tags = Tag.objects.all()
        sortedTags = sorted(tags, key=lambda x: x.label)
        serializer = TagSerializer(sortedTags, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized tag instance
        """
        new_tag = Tag()
        new_tag.label = request.data["label"]

        new_tag.save()

        serializer = TagSerializer(new_tag, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a tag
        Returns:
            Response -- Empty body with 204 status code
        """
        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]

        tag.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single tag
        Returns:
            Response -- 200, 404, or 500 status code
        """
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags
    Arguments:
        serializer type
    """
    class Meta:
        model = Tag
        fields = ('id', 'label')