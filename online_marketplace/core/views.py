from django.shortcuts import render
from item.models import Category, Item

# Create your views here.

def index(response):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(response, 'core/index.html', {'items':items, 'categories':categories})

def contact(response):
    return render(response, 'core/contact.html')