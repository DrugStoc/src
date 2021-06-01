from rest_framework import generics, authentication, permissions

from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, viewsets, mixins
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist

from .models import CartItem

from .serializer import AddCartSerializer, UserCartSerializer


class AddItemToCart(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = AddCartSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        ids = data.get('ids')
        try:
            cod  = CartItem.objects.get(ids=ids, is_checkedout=False)
        except ObjectDoesNotExist:
            serializer = AddCartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)
            return Response({"message": "item added to cart successfully", "status": 200, "data": serializer.data}, status=200)
        else:
            return Response({"message": "Item already exist in cart", "status": 401}, status=401)
        return Response({"message": "Invalid Request", "status": 400}, status=400)

    def list(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 2000
        queryset = self.get_queryset().filter(user=self.request.user, is_checkedout=False)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = UserCartSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class UpdateItemCart(generics.RetrieveUpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = UserCartSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class DeleteItemCart(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = UserCartSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
