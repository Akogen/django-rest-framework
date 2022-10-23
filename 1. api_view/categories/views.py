from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
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
            created_category = serializer.save()
            return Response(
                CategorySerializer(created_category).data,
            )
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        category_detail = Category.object.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        serializer = CategorySerializer(category_detail)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CategorySerializer(
            category_detail,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(
                CategorySerializer(updated_category).data,
            )
        else:
            return Response(serializer.errors)
    elif request.method == "DELETE":
        category_detail.delete()
        return Response(status=HTTP_204_NO_CONTENT)