from django.urls import path
from .views import rockets_launches_view

urlpatterns = [
    path('', rockets_launches_view, name='rockets_launches'),
]
