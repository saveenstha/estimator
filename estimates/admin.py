from django.contrib import admin
from .models import *

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit', 'rate']
    list_filter = ['category']
    search_fields = ['name']

admin.site.register(MaterialCategory)
admin.site.register(Procurement)
admin.site.register(EstimateComponent)
