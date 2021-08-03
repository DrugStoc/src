from django.urls import path, include

from . import views

app_name = 'products'

urlpatterns = [
    path('products', views.ProductsList.as_view(), name="all_products"),
    path('products/<int:pk>', views.ProductDetail.as_view(), name="all_products"),
    path('category', views.CategoryList.as_view(), name="all_category"),
    path('category/<int:pk>', views.ProductPerCatgory.as_view(), name="product_category"),
    path('orders', views.UserOrder.as_view(), name="user_orders"),
    path('rep_orders', views.RepOrder.as_view(), name="rep_orders"),
    path('orders/<int:pk>', views.UserOrderDetail.as_view(), name="user_orders"),
    path('invoice', views.UserInvoice.as_view(), name="user_invoice"),
    path('odoo-manufacturer', views.ManufacturerList.as_view(), name="odoo_manufacturer"),
    path('manufacturer', views.BrandList.as_view(), name="manufacturer"),
    path('manufacturer/<str:name>', views.ProductPerManufacturer.as_view(), name="product_manufacturer"),
    # path('manufacturer/<str:name>/search', views.SearchManufacturerList.as_view(), name="search product brand"),
    path('search', views.SearchResultList.as_view(), name="search"),
    path('create-order', views.CreateOrder.as_view(), name="create order"),
    path('sync_user', views.SyncUser.as_view(), name="sync user"),
    path('bulk_manufacturers', views.Bulk_Manufacturers.as_view(), name="sync manufacturers"),
    path('sale_overview', views.SalesRep_Activities.as_view(), name="sync manufacturers"),
    path('recievables', views.RepReceivables.as_view(), name="sync manufacturers"),
    path('sale_customer', views.SalesRep_Customer.as_view(), name="sync manufacturers"),
    path('account_statement/<int:id>', views.Customer_Statement.as_view(), name="sync manufacturers"),
    path('user_statement', views.User_Statement.as_view(), name="user statement"),
    path('user_profile', views.User_Account.as_view(), name="user profile"),
]