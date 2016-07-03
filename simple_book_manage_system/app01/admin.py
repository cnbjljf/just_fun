from django.contrib import admin
from app01 import models

# Register your models here.
admin.site.register(models.author)
admin.site.register(models.book)
admin.site.register(models.publisher)