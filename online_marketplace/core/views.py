from django.shortcuts import render

# Create your views here.

def index(response):
    return render(response, 'core/index.html')

def contact(response):
    return render(response, 'core/contact.html')