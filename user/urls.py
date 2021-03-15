from django.urls import path, include

from . import views

app_name = 'user'

urlpatterns = [
    path('register', views.CreateUserView.as_view(), name="create"),
    path('login/', views.CreateTokenView.as_view(), name="token"),
    path('user/', views.ManageUserView.as_view(), name="me"),
    # path('auth/', include('djoser.urls')),
    path('documents/', views.DocumentList.as_view(), name="upload"),
    path('users/', views.UserList.as_view(), name="users"),
    path('verify/', views.VerifyOtp.as_view(), name="verify"),
]