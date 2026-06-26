from django.urls import path

from . import views

app_name = "produtos"

urlpatterns = [
    path("", views.produto_list_page, name="list_page"),
    path("novo/", views.produto_create, name="create"),
    path("<int:pk>/", views.produto_detail_page, name="detail_page"),
    path("<int:pk>/editar/", views.produto_update, name="update"),

    path("api/", views.produto_list_api, name="api_list"),
    path("api/<int:pk>/", views.produto_detail_api, name="api_detail"),
    path("api/<int:pk>/excluir/", views.produto_delete_api, name="api_delete"),
]
