from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view),
    path('api/', views.home_view),
    path('api/v1/', views.home_view)
]