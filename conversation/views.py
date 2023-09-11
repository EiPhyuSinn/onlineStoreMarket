from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from items.models import Item
from .forms import ConversationMesageForm
from .models import Conversation

@login_required
def new_conversation(request,item_pk):
  
    item = get_object_or_404(Item,pk=item_pk)
    
    if item.created_by == request.user:
        return redirect('dashboard:inbox')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])
    
    
    if conversations:
        pass 
    if request.method == 'POST':
       
        form = ConversationMesageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation =conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('items:detail',pk=item_pk)
    else:
        form = ConversationMesageForm()

        return render(request,'newConversation.html',{
            'form':form
        })
    
@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members=request.user.id)
    return render(request,'inbox.html',{
                  'conversations':conversations
                  }) 

@login_required
def detail(request,pk):
    
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    form = ConversationMesageForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation =conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('conversation:detail',pk=pk)
    return render(request,'detail.html',{
        'conversation' : conversation,
        'form' : form
    })
