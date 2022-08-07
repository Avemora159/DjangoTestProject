from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserAuthorization.as_view(), name='auth_page'),
]
