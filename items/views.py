from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Item,Category
from .forms import NewItemForm,EditItemForm
# Create your views here.

def detail_view(request,pk):
    
   
    item = get_object_or_404(Item,pk=pk)
    related_items = Item.objects.filter(category=item.category,is_sold=False).exclude(pk=pk)[0:3]
#     return HttpResponse(request,'hi there testing')
    return render(request,'details.html',{
          'item' : item,
          'related_items' : related_items
    }) 

@login_required
def newItem(request):
    
      form = NewItemForm(request.POST,request.FILES)
      if request.method == 'POST':
            if form.is_valid():
                  item = form.save(commit=False)
                  item.created_by = request.user
                  item.save()
                  return redirect('items:detail',pk=item.id)
            else:
                 form = NewItemForm()
      
      return render(request,'form.html',{
            'form':form
    })

@login_required
def delete(request,pk):
     item = get_object_or_404(Item,pk=pk)
     item.delete()
     return redirect('dashboard:index')

@login_required
def edit(request,pk):
     item = get_object_or_404(Item,pk=pk)
     form = EditItemForm(instance=item)
     if request.method == 'POST':
      form = EditItemForm(request.POST,request.FILES,instance=item)
      if form.is_valid():
            form.save()
            return redirect('items:detail',pk=item.id)
      
     return render(request,'edit.html',{
          'form' : form
     })

# for browsing

def items(request):
     query = request.GET.get('query','')
     category_id = request.GET.get('category',0)
     categories = Category.objects.all()
     items = Item.objects.filter(is_sold=False)
     if category_id:
          items = items.filter(category_id = category_id)
     if query:
          items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
          
      
     return render(request,'items.html',{
           'items' : items,
           'query' : query,
           'categories' : categories,
           'category_id' : int(category_id)
      })

