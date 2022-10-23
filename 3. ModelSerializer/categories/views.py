from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer


class Categories(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            created_category = serializer.save()
            return Response(
                CategorySerializer(created_category).data,
            )
        else:
            return Response(serializer.errors)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            category_detail = Category.object.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound
        return category_detail

    def get(self, request, pk):
        category_detail = self.get_object(pk)
        serializer = CategorySerializer(category_detail)
        return Response(serializer.data)

    def put(self, request, pk):
        category_detail = self.get_object(pk)
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

    def delete(self, rquest, pk):
        category_detail = self.get_object(pk)
        category_detail.delete()
        return Response(status=HTTP_204_NO_CONTENT)
