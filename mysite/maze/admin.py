from django.contrib import admin

# Register your models here.
from .models import ServiceProvider

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'clicks', 'impressions')
    search_fields = ('name', 'contact_info')
    list_filter = ('clicks', 'impressions')

# maze/admin.py
# maze/admin.py

from django.contrib import admin
from .models import Category, SubCategory, Service

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    #search_fields = ('name', 'category__name')
    list_filter = ('category',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subcategory', 'created_at')
    search_fields = ('title', 'description', 'subcategory__name')
    list_filter = ('subcategory__category', 'subcategory')

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Service, ServiceAdmin)



