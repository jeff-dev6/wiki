from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [

    path("", views.index, name="index"),
    path("new_page", views.new_page, name="new_page"),
    path("search", views.search, name="search"),
    path("random/", views.random_page, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("edit/<str:title>", views.edit, name="edit"),
]
