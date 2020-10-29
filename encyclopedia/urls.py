from django.urls import path

from . import views

#app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.get_wiki, name="get_wiki"),
    path("search/", views.search, name="search"),

    path("create/", views.create, name="create"),
    #
    path("edit/<title>", views.edit, name="edit"),
    path("random/", views.randompage, name="random")
]
