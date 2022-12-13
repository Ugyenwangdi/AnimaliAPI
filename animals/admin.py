from django.contrib import admin

from .models import Animal, Page # , Contributor

# Register your models here.
admin.site.register(Animal)
admin.site.register(Page)

# admin.site.register(Contributor)
