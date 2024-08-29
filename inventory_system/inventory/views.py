from accounts.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Products, SubVariant
from .serializers import ProductsSerializer, AddStockSerializer, RemoveStockSerializer


class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            products = Products.objects.all()
            serializer = ProductsSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({'message': 'Product created successfully', 'product_id': product.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProductsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            products = Products.objects.filter(CreatedUser=user)
            serializer = ProductsSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f'Error: {e}')
            return Response({'detail': 'An error occurred while fetching products.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddStockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddStockSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            size = serializer.validated_data['size']
            color = serializer.validated_data['color']
            stock_to_add = serializer.validated_data['stock']

            try:
                subvariant = SubVariant.objects.get(
                    product=product,
                    size=size,
                    color=color
                )
                subvariant.stock += stock_to_add
                subvariant.save()
                return Response({'message': 'Stock updated successfully'}, status=status.HTTP_200_OK)
            except SubVariant.DoesNotExist:
                return Response({'error': 'Subvariant not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveStockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RemoveStockSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            size = serializer.validated_data['size']
            color = serializer.validated_data['color']
            stock_to_remove = serializer.validated_data['stock']

            try:
                subvariant = SubVariant.objects.get(
                    product=product,
                    size=size,
                    color=color
                )
                if subvariant.stock >= stock_to_remove:
                    subvariant.stock -= stock_to_remove
                    subvariant.save()
                    return Response({'message': 'Stock removed successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Insufficient stock to remove'}, status=status.HTTP_400_BAD_REQUEST)
            except SubVariant.DoesNotExist:
                return Response({'error': 'Subvariant not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
