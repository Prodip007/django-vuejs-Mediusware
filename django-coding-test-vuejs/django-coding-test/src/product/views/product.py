from typing import Any, Dict
from django.views import generic
from django.shortcuts import get_object_or_404
from django.db.models import Q
# from django.views.generic import ListView

from product.models import Variant, Product, ProductVariant, ProductVariantPrice


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    

class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    paginate_by = 2


    def get_queryset(self, *args, **kwargs):
        if self.request.GET == {} or self.request.GET.get('page'):
            return super().get_queryset()
        else:
            product_name = self.request.GET.get('title', None)
            product_variant = self.request.GET.get('variant', None)
            price_from = self.request.GET.get('price_from',None)
            price_to = self.request.GET.get('price_to')
            object_list = []

            if product_name:
                object_list = Product.objects.filter(title=product_name)
            elif product_variant:
                object_list = Product.objects.filter(productvariant=product_variant)
            elif price_from or price_to:
                productvariantprice_list = []
                if price_from:
                    s_productvariantprice_list = ProductVariantPrice.objects.filter(price__gt=price_from)
                    for item in s_productvariantprice_list:
                        productvariantprice_list.append(item)
                if price_to:
                    s_productvariantprice_list = ProductVariantPrice.objects.filter(price__lt=price_to)
                    for item in s_productvariantprice_list:
                        productvariantprice_list.append(item)
                for item in productvariantprice_list:
                    s_obj = get_object_or_404(Product, productvariantprice=item)
                    if s_obj not in object_list:
                        object_list.append(s_obj)
            return object_list            

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True)
        context['variants'] = list(variants)
        return context
    
