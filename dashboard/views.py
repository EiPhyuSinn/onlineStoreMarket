from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from items.models import Item

# Create your views here.

@login_required
def index(request):
    # return render(request,'dashboard/index.html')
    items = Item.objects.filter(created_by = request.user)
    return render(request,'dashboard/index.html',{
        'items' : items,
    })
