from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("imoveis/", views.properties, name="properties"),
    path("imovel/<int:pk>/", views.detail, name="detail"),
    path("api/sugestoes-endereco/", views.address_suggestions, name="address_suggestions"),
]
