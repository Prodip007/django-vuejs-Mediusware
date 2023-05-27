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

    def get_queryset(self, *args, **kwargs):
        if self.request.GET:
            product_name = self.request.GET.get('title', None)
            product_variant = self.request.GET.get('variant', None)
            object_list = []

            if product_name:
                object_list = Product.objects.filter(title=product_name)
                for obj in object_list:
                    print(obj.productvariant_set.all())
            elif product_variant:
                object_list = Product.objects.filter(productvariant=product_variant)
            return object_list
        

        else:
            return super().get_queryset()

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True)
        context['variants'] = list(variants)
        return context
    
