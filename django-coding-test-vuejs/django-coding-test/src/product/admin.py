from django.contrib import admin

from .models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice

# Register your models here.

admin.site.register({Variant, Product, ProductImage, ProductVariant, ProductVariantPrice})
