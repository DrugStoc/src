from rest_framework import generics, authentication, permissions

from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, viewsets, mixins
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist

from .models import MyDrugStocItem

from .serializer import CreateDraftSerializer, myDrugStocSerializer, DraftSerializer


class AddItemToDraft(generics.ListCreateAPIView):
    queryset = MyDrugStocItem.objects.all()
    serializer_class = CreateDraftSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data.get('items')
        bulk = []
        for item in data:
            data =  self.get_queryset().filter(user=request.user, ids=item['ids'])
            if not data:
                MyDrugStocItem.objects.create(user=request.user, **item)
        MyDrugStocItem.objects.bulk_create(bulk, ignore_conflicts=True)
        return Response({"message": "Draft Created"}, status=201)

    def list(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 20
        queryset = self.get_queryset().filter(user=self.request.user, is_Draft=False)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = DraftSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class UpdateItemMydrugStoc(generics.RetrieveUpdateAPIView):
    queryset = MyDrugStocItem.objects.all()
    serializer_class = DraftSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class DeleteItemCartMydrugstoc(generics.DestroyAPIView):
    queryset = MyDrugStocItem.objects.all()
    serializer_class = DraftSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

# class ListMyDrugStocDraft(generics.ListAPIView):
#     queryset = MyDrugStocItem.objects.all()
#     serializer_class = myDrugStocSerializer
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)

        # serializer = myDrugStocSerializer(request.data)
        # return Response({"message": "item added to cart successfully", "status": 200, "data": data}, status=200)
        # ids = data.get('ids')
        # try:
        #     cod  = CartItem.objects.get(ids=ids, is_checkedout=False)
        # except ObjectDoesNotExist:
        #     serializer = AddCartSerializer(data=request.data)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save(user=self.request.user)
        #     return Response({"message": "item added to cart successfully", "status": 200, "data": serializer.data}, status=200)
        # else:
        #     return Response({"message": "Item already exist in cart", "status": 401}, status=401)
        # return Response({"message": "Invalid Request", "status": 400}, status=400)

    #     [
    #     {
    #         "name": "ddd",
    #         "image": "ddd",
    #         "ids": 22,
    #         "quantity": 22,
    #         "price": "22.00",
    #     },
    #     {
    #         "name": "ee",
    #         "image": "ee",
    #         "ids": 33,
    #         "quantity": 33,
    #         "price": "33.00",
    #     }
    # ]