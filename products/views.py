from xmlrpc import client as xmlrpclib
import socket
import json

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model, authenticate
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from django.utils.timezone import now
from rest_framework.parsers import MultiPartParser


from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, viewsets, mixins

from .uil import return_products as get_object, return_categories, return_manufacturer, return_orders, return_order_details, return_response, return_user

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from .serializers import ProductSerializer, CategorySerializer, ManfacturerSerializer, orderSerializer, CreateOrderSerializer, syncUserSerializer, BulkManufacturers

from product.models import ProductModel

from user.models import User

from manufacturers.models import ManufacturerModel

from django.contrib.auth import get_user_model, authenticate


# url = 'http://drugstoc-sam-dev-1293660.dev.odoo.com'
# db = 'drugstoc-sam-dev-1293660'
# username = 'ronyek@gmail.com'
# password = 'mko0nji9'

# url = 'http://drugstoc.odoo.com'
# db = 'drugstoc-main-master-86674'
# username ='licensemgr@drugstoc.com'
# password = 'mko0nji9'

url = 'http://drugstoc.odoo.com'
db = 'drugstoc-main-master-86674'
username ='app@drugstoc.com'
password = 'app123456'




class ProductsList(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    
    def list(self, request):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        page = request.query_params.get('page')
        page_number = 0 if page == None else int(page) - 1
        offset = page_number * 50
        total = models.execute_kw(db, uid, password,
        'product.product', 'search_count',
        [[
            ['company_id', '=', 1 ],
            [ 'sale_ok', '=', True ],
            [ 'website_published', '=', True ],
        ]])
        data = models.execute_kw(
            db, uid, password, 
            'product.product', 'search_read', 
            [[
                [ 'company_id', '=', 1 ],
                [ 'sale_ok', '=', True ],
                [ 'website_published', '=', True ],
            ]], 
            {'fields': 
                [
                    'id',
                    'name', 
                    'list_price',
                    'qty_available',
                    'x_studio_field_5Gttm',
					'x_studio_field_xH9Vy',
                    'create_date',
                    'description',
                    'categ_id',
                    # 'image',
                ], 'limit': 50, 'offset': offset})
        result = map(get_object, data)
        return return_response(request, result, total, offset)
        # print(request.build_absolute_uri(''))
        # return Response({"count": total,  "previous": uro, "next": None, "results": result}, status=200)

class ProductDetail(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


    def list(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        total = models.execute_kw(db, uid, password,
        'product.product', 'search_count',
        [[
            ['company_id', '=', 1 ],
            [ 'sale_ok', '=', True ],
            [ 'website_published', '=', True ],
            [ 'id', '=', pk  ],
        ]])
        data = models.execute_kw(
            db, uid, password, 
            'product.product', 'search_read', 
            [[
                [ 'company_id', '=', 1 ],
                [ 'sale_ok', '=', True ],
                [ 'website_published', '=', True ],
                [ 'id', '=', pk  ],
            ]], 
            {'fields': 
                [
                    'id',
                    'name', 
                    'list_price',
                    'qty_available',
                    'x_studio_field_5Gttm',
					'x_studio_field_xH9Vy',
                    'create_date',
                    'description',
                    'categ_id',
                ], 'limit': 25})
        # result = map(get_object, data)
        return Response({"count": total,  "previous": '', "next": "", "results": data[0]}, status=200)

class CategoryList(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def list(self, request):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        page = request.query_params.get('page')
        page_number = 0 if page == None else int(page) - 1
        offset = page_number * 50
        total = models.execute_kw(db, uid, password,
        'product.category', 'search_count',
        [[
            [1, '=', 1 ]
        ]])
        data = models.execute_kw(
            db, uid, password, 
            'product.category', 'search_read', 
            [[
                [ 1, '=', 1 ],
            ]], 
            {'fields': 
                [
                    'id',
                    'name', 
                    "product_count",
                    "create_date",
                ], 'limit': 50, 'offset': offset}
            )
        result = map(return_categories, data)
        return return_response(request, result, total, offset)

class ManufacturerList(generics.ListAPIView):
        queryset = ManufacturerModel.objects.all()
        serializer_class = ManfacturerSerializer
        authentication_classes = (authentication.TokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated,)

        def list(self, request):
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
            data = models.execute_kw(
                db, uid, password, 
                'product.product', 'search_read', 
                [[
                    ['company_id', '=', 1 ],
                    [ 'sale_ok', '=', True ],
                    [ 'website_published', '=', True ],
                ]],
                {'fields': 
                    [
                        'x_studio_field_xH9Vy',
                    ]})
            res = list({v['x_studio_field_xH9Vy']: v for v in data}.values())
            resp = map(return_manufacturer, res)
            results = sorted(resp, key=lambda x: x['name'].lower())

            return Response({"count": len(res),  "previous": '', "next": "", "results": results}, status=200)

class SearchResultList(generics.ListAPIView):
        queryset = ManufacturerModel.objects.all()
        serializer_class = ManfacturerSerializer
        authentication_classes = (authentication.TokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated,)

        def list(self, request):
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
            search = request.query_params.get('products')
            data_name = models.execute_kw(
                db, uid, password, 
            'product.product', 'search_read', 
            [[
                [ 'company_id', '=', 1 ],
                [ 'sale_ok', '=', True ],
                [ 'website_published', '=', True ],
                [ 'name', 'ilike', search],
            ]], 
            {'fields': 
                [
                    'id',
                    'name', 
                    'list_price',
                    'qty_available',
                    'x_studio_field_5Gttm',
					'x_studio_field_xH9Vy',
                    'create_date',
                    'description',
                    'categ_id',
                ], "limit": 100})
            data_composition = models.execute_kw(
                db, uid, password, 
            'product.product', 'search_read', 
            [[
                [ 'company_id', '=', 1 ],
                [ 'sale_ok', '=', True ],
                [ 'website_published', '=', True ],
                [ 'x_studio_field_5Gttm', 'ilike', search],
            ]], 
            {'fields': 
                [
                    'id',
                    'name', 
                    'list_price',
                    'qty_available',
                    'x_studio_field_5Gttm',
					'x_studio_field_xH9Vy',
                    'create_date',
                    'description',
                    'categ_id',
                ], "limit": 100})
            data_manufacturer = models.execute_kw(
                db, uid, password, 
            'product.product', 'search_read', 
            [[
                [ 'company_id', '=', 1 ],
                [ 'sale_ok', '=', True ],
                [ 'website_published', '=', True ],
                [ 'x_studio_field_xH9Vy', 'ilike', search],
            ]], 
            {'fields': 
                [
                    'id',
                    'name', 
                    'list_price',
                    'qty_available',
                    'x_studio_field_5Gttm',
					'x_studio_field_xH9Vy',
                    'create_date',
                    'description',
                    'categ_id',
                ], "limit": 100})
            a = [y for x in [data_name, data_composition, data_manufacturer] for y in x]
            name = map(get_object, data_name)
            composition = map(get_object, data_composition)
            brand = map(get_object, data_manufacturer)
            all_data = map(get_object, a)
            return Response({"count": "",  "previous": '', "next": "", "results": { "all": all_data, "product_name": name, "product_composition": composition, "product_brand": brand }}, status=200)

class BrandList(generics.ListAPIView):
        queryset = ManufacturerModel.objects.all().order_by('priority')
        serializer_class = ManfacturerSerializer
        authentication_classes = (authentication.TokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated,)

class ProductPerCatgory(generics.ListAPIView):
        queryset = ProductModel.objects.all()
        serializer_class = ProductSerializer
        authentication_classes = (authentication.TokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated,)

        def list(self, request, *args, **kwargs):
            pk = self.kwargs.get('pk')
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
            page = request.query_params.get('page')
            page_number = 0 if page == None else int(page) - 1
            offset = page_number * 50
            total = models.execute_kw(db, uid, password,
            'product.product', 'search_count',
            [[
                ['company_id', '=', 1 ],
                [ 'sale_ok', '=', True ],
                [ 'website_published', '=', True ],
                [ 'categ_id', '=', pk ],
            ]])
            data = models.execute_kw(
            db, uid, password, 
            'product.product', 'search_read', 
            [[
                [ 'company_id', '=', 1 ],
                [ 'sale_ok', '=', True ],
                [ 'website_published', '=', True ],
                [ 'categ_id', '=', pk ],
            ]], 
            {'fields': 
                [
                    'id',
                    'name', 
                    'list_price',
                    'qty_available',
                    'x_studio_field_5Gttm',
					'x_studio_field_xH9Vy',
                    'create_date',
                    'description',
                    'categ_id',
                ], 'limit': 50, 'offset': offset})
            result = map(get_object, data)
            return return_response(request, result, total, offset)

class ProductPerManufacturer(generics.ListAPIView):
        queryset = ProductModel.objects.all()
        serializer_class = ProductSerializer
        authentication_classes = (authentication.TokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated,)

        def list(self, request, *args, **kwargs):
            pk = self.kwargs.get('name')
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
            page = request.query_params.get('page')
            page_number = 0 if page == None else int(page) - 1
            offset = page_number * 50
            total = models.execute_kw(db, uid, password,
            'product.product', 'search_count',
            [[
                ['company_id', '=', 1 ],
                [ 'sale_ok', '=', True ],
                [ 'website_published', '=', True ],
                [ 'x_studio_field_xH9Vy', 'ilike', pk ],
            ]])
            data = models.execute_kw(
            db, uid, password, 
            'product.product', 'search_read', 
            [[
                [ 'company_id', '=', 1 ],
                [ 'sale_ok', '=', True ],
                [ 'website_published', '=', True ],
                [ 'x_studio_field_xH9Vy', 'ilike', pk ],
            ]], 
            {'fields': 
                [
                    'id',
                    'name', 
                    'list_price',
                    'qty_available',
                    'x_studio_field_5Gttm',
					'x_studio_field_xH9Vy',
                    'create_date',
                    'description',
                    'categ_id',
                ], 'limit': 50, 'offset': offset})
            result = map(get_object, data)
            return return_response(request, result, total, offset)

class UserOrder(generics.ListAPIView):
        queryset = ProductModel.objects.all()
        serializer_class = ProductSerializer
        authentication_classes = (authentication.TokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated,)

        def list(self, request, *args, **kwargs):
            user = request.user.erp_id;
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
            page = request.query_params.get('page')
            page_number = 0 if page == None else int(page) - 1
            offset = page_number * 50
            total = models.execute_kw(db, uid, password,
            'sale.order', 'search_count',
            [[
                ['partner_id', '=', user ],
            ]])
            data = models.execute_kw(
            db, uid, password, 
            'sale.order', 'search_read', 
            [[
                ['partner_id', '=', user ],
            ]], 
            {'fields': 
                [
                    'id',
                    'name', 
                    "state",
                    "date_order",
                    "user_id",
                    "partner_id",
                    "amount_untaxed",
                    "amount_tax",
                    "amount_total",
                    "payment_term_id",
                    "date_order",
                    "order_line"
                ], 'limit': 50, 'offset': offset})
            result = map(return_orders, data)
            return return_response(request, result, total, offset)

class UserOrderDetail(generics.ListAPIView):
        queryset = ProductModel.objects.all()
        serializer_class = ProductSerializer
        authentication_classes = (authentication.TokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated,)

        def list(self, request, *args, **kwargs):
            pk = self.kwargs.get('pk')
            user = request.user.erp_id;
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
            page = request.query_params.get('page')
            page_number = 0 if page == None else int(page) - 1
            offset = page_number * 50
            total = models.execute_kw(db, uid, password,
            'sale.order.line', 'search_count',
            [[
                ['order_partner_id', '=', user ],
                ['order_id', '=', pk ],
            ]])
            data = models.execute_kw(
            db, uid, password, 
            'sale.order.line', 'search_read', 
            [[
                ['order_partner_id', '=', user ],
                ['order_id', '=', pk ],
            ]], 
            {'fields': 
                [
                    'id',
                    'name', 
                    "price_unit",
                    "price_subtotal",
                    "price_total",
                    "product_id",
                    "product_uom_qty",
                    "salesman_id",
                    "order_partner_id",
                    "state",
                    "create_date"
                ], 'limit': 50, 'offset': offset})
            result = map(return_order_details, data)
            return return_response(request, result, total, offset)

class UserInvoice(generics.ListAPIView):
        queryset = ProductModel.objects.all()
        serializer_class = ProductSerializer
        authentication_classes = (authentication.TokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated,)

        def list(self, request, *args, **kwargs):
            user = request.user.erp_id;
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
            page = request.query_params.get('page')
            page_number = 0 if page == None else int(page) - 1
            offset = page_number * 50
            total = models.execute_kw(db, uid, password,
            'res.partner', 'search_count',
            [[
                # ['partner_id', '=', user ],
            ]])
            data = models.execute_kw(
            db, uid, password, 
            'res.partner', 'search_read', 
            [[
                # ['partner_id', '=', user ],
            ]], 
            {'fields': 
                [
                    # 'id',
                    # 'name', 
                    # "price_unit",
                    # "price_subtotal",
                    # "price_total",
                    # "product_id",
                    # "product_uom_qty",
                    # "salesman_id",
                    # "order_partner_id",
                    # "state",
                    # "create_date"
                ],'limit': 5, 'offset': offset})
            result = map(return_order_details, data)
            return return_response(request, data, total, offset)

class SyncUser(generics.CreateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = syncUserSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = request.data.get('items')
        # user = request.user.erp_id
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        params = models.execute_kw(db, uid, password,
            'res.partner', 'search_read',
            [ {
                # 'partner_id' : user,
                # 'partner_share', '=', True
            }],{'fields': 
                [
                    'id',
                    'name', 
                    'email',
                    'x_studio_field_vM2kZ',
                    "mobile",
                    "price_subtotal",
                    "phone",
                ],'limit': 3})

        resp = map(return_user, params)
        users = list(resp)
        print(users);
        # for item in users:
        #     print(item)
        #     get_user_model().objects.create_user(email=item['email'])
        # print(u)
        get_user_model().objects.bulk_create([User(**each) for each in users])
        return Response({"message": "User synced"}, status=201)

class CreateOrder(generics.CreateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = CreateOrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    

    def post(self, request):
        data = request.data.get('items')
        user = request.user.erp_id
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        params = models.execute_kw(db, uid, password,
            'sale.order', 'create',
            [ {
                'partner_id' : user,
                # 'user_id': user
            }])
        def create_order(n):
            return {
                'order_id': params,
                'product_id': n['ids'],
                'name':n['name'],
                'product_uom_qty': n['quantity'],
            }
        result = map(create_order, data)
        orders = list(result)
        print(orders)
        for l in orders:
            params2 = models.execute_kw(db, uid, password,'sale.order.line', 'create',[l]);
        return Response({"message": "Draft Created", "data": result, "user": user, "params2": params2}, status=201)

class Bulk_Manufacturers(generics.CreateAPIView):
    queryset = ManufacturerModel.objects.all()
    serializer_class = BulkManufacturers
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data.get('lists')
        # bulk = []
        # for item in data:
        #     data =  self.get_queryset()
        #     if not data:
        #         ManufacturerModel.objects.create(**item)
        ManufacturerModel.objects.bulk_create([ManufacturerModel(**each) for each in data])
        return Response({"message": "success"}, status=201)
