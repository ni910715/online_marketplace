from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SignupForm

# Create your views here.

def index(response):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(response, 'core/index.html', {'items':items, 'categories':categories})

def contact(response):
    return render(response, 'core/contact.html')

def signup(response):
    if response.method == 'POST':
        form = SignupForm(response.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()
    
    return render(response, 'core/signup.html', {'form':form})