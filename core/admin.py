from django.contrib import admin
from .models import Property
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display=("id","title","price","typology","location")
    search_fields=("title","location","typology","description")
    list_filter=("typology",)
