from django.contrib import admin
from resources.models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'module', 'uploaded_by')
    list_filter = ('resource_type', 'module')
    search_fields = ('title',)
