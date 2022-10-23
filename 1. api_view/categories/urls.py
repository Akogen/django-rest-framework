from django.urls import path
from . import views

urlpatterns = [
    path("", views.Categories),
    path("<int:pk>", views.Category),
]
