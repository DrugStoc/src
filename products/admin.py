from django.contrib import admin

from product.models import ProductModel
from manufacturers.models import ManufacturerModel
from categories.models import CategoryModel


class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'priority', 'image',)
    list_display = ('name', 'priority', 'image',)



admin.site.register(ProductModel)
admin.site.register(ManufacturerModel, ManufacturerAdmin)
admin.site.register(CategoryModel)