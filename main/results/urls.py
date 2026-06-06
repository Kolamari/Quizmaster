from django.urls import path
from . import views

urlpatterns = [
    path('', views.results_redirect, name='results_index'),
]
