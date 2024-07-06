from django.urls import path
from . import views

app_name = "item"
urlpatterns = [
    path("", views.items, name="items"),
    path("<int:pk>/", views.detail, name="detail"),
    path("new/", views.new, name="new"),
    path("delete/<int:pk>/", views.delete, name="delete"),
    path("edit/<int:pk>/", views.update, name="edit"),
]
