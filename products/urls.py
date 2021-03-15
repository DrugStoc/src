from django.urls import path, include

from . import views

app_name = 'products'

urlpatterns = [
    path('products', views.ProductsList.as_view(), name="all_products"),
    path('products/<int:pk>', views.ProductDetail.as_view(), name="all_products"),
    path('category', views.CategoryList.as_view(), name="all_category"),
    path('category/<int:pk>', views.ProductPerCatgory.as_view(), name="product_category"),
    path('orders', views.UserOrder.as_view(), name="user_orders"),
    path('orders/<int:pk>', views.UserOrderDetail.as_view(), name="user_orders"),
    path('invoice', views.UserInvoice.as_view(), name="user_invoice"),
    path('odoo-manufacturer', views.ManufacturerList.as_view(), name="odoo_manufacturer"),
    path('manufacturer', views.BrandList.as_view(), name="manufacturer"),
    path('manufacturer/<str:name>', views.ProductPerManufacturer.as_view(), name="product_manufacturer"),
    path('search', views.SearchResultList.as_view(), name="search"),
    path('create-order', views.CreateOrder.as_view(), name="create order"),
]