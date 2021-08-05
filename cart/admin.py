from django.contrib import admin
from . import models

class cartAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_checkedout')
    actions = ['make_published']
    def make_published(self, request, queryset):
        queryset.update(is_checkedout=False)
    make_published.short_description = "Mark selected stories as not checkout"

admin.site.register(models.CartItem, cartAdmin)
