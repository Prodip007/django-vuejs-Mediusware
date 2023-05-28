from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.models import Variant, Product, ProductVariant, ProductVariantPrice

class CreateProductView(generic.CreateView):
    template_name = 'products/create.html'
    model = Product
    fields = "__all__"

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

# @csrf_exempt    
@api_view(['POST'])
def create_product_apiview(request):
    message = "Got some data!"
    product_title = request.data.get('title')
    product_sku = request.data.get('sku')
    product_description = request.data.get('description')
    product_image = request.data.get('product_image')
    product_variant = request.data.get('product_variant')
    product_variant_prices = request.data.get('product_variant_prices')
    if product_title:
        product_obj = Product.objects.create(title=product_title, sku=product_sku, description=product_description)
        # if product_variant:
        #     product_variant_obj = ProductVariant.objects.create(variant_title=product_variant_prices) 
        print(product_obj)
    else:
        message = "Error: Product title is required"
    print('product_image: ', product_image)
    print('product_variant: ', product_variant)
    print('product_variant_prices: ', product_variant_prices)
    return Response({"message": message, "data": request.data})
    # return render_to_response(context_instance=RequestContext(request))

    

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
            price_to = self.request.GET.get('price_to', None)
            product_date = self.request.GET.get('date', None)
            object_list = []

            if product_name:
                s_object_list = Product.objects.filter(title=product_name)
                for item in s_object_list:
                    if item not in object_list:
                        object_list.append(item)
            if product_variant:
                s_object_list = Product.objects.filter(productvariant=product_variant)
                for item in s_object_list:
                    if item not in object_list:
                        object_list.append(item)
            if price_from or price_to:
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
            if product_date:
                s_obj = Product.objects.filter(created_at__date=product_date)
                for item in s_obj:
                    if s_obj not in object_list:
                        object_list.append(item)
            return object_list            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True)
        context['variants'] = list(variants)
        return context
    
