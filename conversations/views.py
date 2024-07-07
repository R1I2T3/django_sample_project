from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm
# Create your views here.


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    if item.created_by == request.user:
        return redirect("dashboard:index")
    conversations = Conversation.objects.filter(item=item).filter(
        members__in=[request.user.id]
    )
    if conversations:
        # return redirect("conversation:details",pk=conversations.id)
        pass
    if request.method == "POST":
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversations = Conversation.objects.create(item=item)
            conversations.members.add(request.user)
            conversations.members.add(item.created_by)
            conversations.save()
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversations
            conversation_message.created_by = request.user
            conversation_message.save()
            return redirect("item:detail", pk=item_pk)
    else:
        form = ConversationMessageForm()
    return render(request, "conversations/new.html", {"form": form})


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user])
    return render(request, "conversations/index.html", {"conversations": conversations})


@login_required
def details(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user]).get(pk=pk)
    if request.method == "POST":
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            print("i am here")
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            return redirect("conversation:details", pk=pk)
    else:
        form = ConversationMessageForm()
    return render(
        request,
        "conversations/details.html",
        {"conversation": conversation, "form": form},
    )
