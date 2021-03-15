from django.urls import path, include

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.AddItemToCart.as_view(), name="add_to_cart"),
    path('<int:pk>', views.UpdateItemCart.as_view(), name="update_item_in_cart"),
    path('<int:pk>/remove', views.DeleteItemCart.as_view(), name="delete_item_in_cart"),
    # path('mycart', views.GetCartItem.as_view(), name="user_cart"),
]