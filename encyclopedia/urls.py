from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.view_entry,name="entry"),
    path("search/",views.search,name="search"),
    path("newpage/",views.newpage,name="newpage"),
    path("edit/",views.edit_page,name="edit_page"),
    path("save/",views.save,name="save"),
    path("random/",views.random_page,name="random_page")

]
