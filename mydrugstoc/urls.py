from django.urls import path, include

from . import views

app_name = 'mydrugstoc'

urlpatterns = [
    path('', views.AddItemToDraft.as_view(), name="create_my_drugstoc_draft"),
    path('<int:pk>', views.UpdateItemMydrugStoc.as_view(), name="update_item_in_mydrugstoc"),
    path('<int:pk>/remove', views.DeleteItemCartMydrugstoc.as_view(), name="delete_item_in_delete"),
]