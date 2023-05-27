from typing import Any, Dict
from django.views import generic
from django.views.generic import ListView

from product.models import Variant, Product, ProductVariant, ProductVariantPrice


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # total_product = Product.objects.all().values('id', 'product_variant_one', 'product_variant_two', 'product_variant_three', 'price', 'stock', 'product')
        # context["variants"] = list(variants)
        return context
