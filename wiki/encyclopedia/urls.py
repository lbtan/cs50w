from django.urls import path

from . import views

## achieves URL namespacing
app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("rand/", views.rand, name="rand"),
    path("ed/", views.edit, name="edit"),
    path("save/", views.save, name="save")
]