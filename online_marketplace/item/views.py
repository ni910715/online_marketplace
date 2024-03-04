from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import NewItemForm

# Create your views here.
def detail(response, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(response, 'item/detail.html', {'item':item, 'related_items':related_items})

@login_required
def new(response):
    if response.method == 'POST':
        form = NewItemForm(response.POST, response.FILES)
        print(form)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.create_by = response.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
    return render(response, 'item/form.html', {'form':form, 'title':'New Item'})