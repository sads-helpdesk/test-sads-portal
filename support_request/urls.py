from django.urls import path
from . import views


urlpatterns = [
    path('new_request/', views.new_request, name='new_request'),

    path('load_clients/', views.load_clients, name='load_clients'),
]