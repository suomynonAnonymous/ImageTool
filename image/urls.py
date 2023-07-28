from django.urls import path
from . import views

urlpatterns = [
    path('', views.process_image, name='process_image'),
    path('result_page/', views.result_page, name='result_page'),
]