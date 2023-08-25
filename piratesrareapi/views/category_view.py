from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from piratesrareapi.models import Category
from django.db.models.functions import Lower

class CategoryView(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for single category
        Returns:
            Response -- JSON serialized category instance
        """
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to categories resource
        Returns:
            Response -- JSON serialized list of categories
        """

        sort_by = request.query_params.get('sort_by', 'label')
        filter_by = request.query_params.get('filter_by', '')

        categories = Category.objects.all().annotate(
            label_lower=Lower('label')
        ).order_by('label_lower')

        if filter_by:
            categories = categories.filter(label__icontains=filter_by)

            categories = categories.order_by(sort_by)

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized category instance or error message
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a category
        Returns:
            Response -- Empty body with 204 status code
        """
        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]

        category.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single category
        Returns:
            Response -- 200, 404, or 500 status code
        """
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')
