from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from items.models import Category,Item
from .forms import SignupForm
from django.contrib.auth import logout
# Create your views here.

def index(request):
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)[0:6]
    # return render(request,'testing.html',{
    #       'categories' : categories,
    #        'items' : items
    #     })
    context = {
        'categories' : categories,
        'items' : items
    }
    return render(request,'index.html',context)


def contact(request):
    return render(request,'contact.html')

def signup(request):
 
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/login')
    return render(request,'signup.html',{
        'form':form
    })

def login(request):
    return HttpResponse(request,'login')

def logout_view(request):
    logout(request)
    return redirect('core:index')