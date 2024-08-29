from django.contrib import admin
from . models import Products,  Color, Size, SubVariant

admin.site.register(Products)
admin.site.register(Size)
admin.site.register(SubVariant)
admin.site.register(Color)
