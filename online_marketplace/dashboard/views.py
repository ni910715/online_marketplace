from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from item.models import Item

# Create your views here.
@login_required
def index(response):
    items = Item.objects.filter(create_by=response.user)
    return render(response, 'dashboard/index.html', {'items':items})