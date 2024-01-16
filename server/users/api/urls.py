from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('get-user/', views.UserView.as_view(), name='get_user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]