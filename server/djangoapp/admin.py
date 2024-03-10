from django.contrib import admin
# from .models import related models
from djangoapp.models import CarMake
from djangoapp.models import CarModel

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
# CarModelAdmin class

class CarModelAdmin(admin.ModelAdmin):
    fields = ['Name', 'Type', 'DealerId', 'Year']
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['Name', 'Description']
    inlines = [CarModelInline]
# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)