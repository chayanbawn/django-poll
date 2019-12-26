from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('values/', views.index),
    path('values/<keys>/', views.index),
]
