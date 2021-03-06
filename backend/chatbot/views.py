from django.shortcuts import render
from store.models import Product
from django.http import JsonResponse

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')

    # Get the reviews
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)
    #JsonResponse(list(products.values()), safe=False)