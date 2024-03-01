from django.shortcuts import render, get_object_or_404
from .models import Item
from .forms import NewItemForm

# Create your views here.
def detail(response, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(response, 'item/detail.html', {'item':item, 'related_items':related_items})

def new(response):
    form = NewItemForm()
    return render(response, 'item/form.html', {'form':form, 'title':'New Item'})