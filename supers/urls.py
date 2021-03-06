from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns 
from .import views

urlpatterns = [
    path('', views.SuperList.as_view()),
    path('<int:pk>/', views.SuperDetail.as_view()),
    path('<int:pk>/<int:pk2>/', views.SuperDetail.as_view()),
    path('<str:super_one>/<str:super_two>/', views.SuperFight.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
