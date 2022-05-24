import imp
from pydoc import importfile
from django.contrib import admin
from .models import Product

# Register your models here.

admin.site.register(Product)