from django.contrib import admin
from django.http import HttpResponse
import csv

from product.models import ProductModel
from manufacturers.models import ManufacturerModel
from categories.models import CategoryModel



class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'priority', 'image',)
    list_display = ('name', 'priority', 'image',)
    actions = ['download_csv']
    def download_csv(self, request, queryset):
        f = open('some.csv', 'w')
        writer = csv.writer(f)
        writer.writerow(['name', 'priority', 'image'])
        for s in queryset:
            writer.writerow([s.name, s.priority, s.image])
        f.close()

        f = open('some.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=manufacturers.csv'
        return response
    download_csv.short_description = "Download CSV file for selected stats."



admin.site.register(ProductModel)
admin.site.register(ManufacturerModel, ManufacturerAdmin)
admin.site.register(CategoryModel)