from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        category = Category.object.get(pk=pk)
    except Category.DoesNotExist:
        raise exceptions.NotFound

    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category = serializer.save()
            serializer = CategorySerializer(category)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)
    elif request.method == "DELETE":
        category.delete()
        return Response(status=status.HTTP_200_OK)
