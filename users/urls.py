# users_app/urls.py

from django.urls import path
from .views import RegisterView, LoginView, UserView, logoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user', UserView.as_view()),
    path('logout/', logoutView.as_view(), name='logout'),
]

