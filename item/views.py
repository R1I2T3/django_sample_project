from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Item, Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, UpdateItemForm
# Create your views here.


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(
        pk=pk
    )[0:3]
    return render(
        request, "item/details.html", {"item": item, "related_items": related_items}
    )


@login_required
def new(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect("item:detail", pk=item.id)
    else:
        form = NewItemForm()
    return render(request, "item/form.html", {"form": form, "title": "New Item"})


@login_required
def update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = UpdateItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("item:detail", pk=pk)
    else:
        form = UpdateItemForm(instance=item)
    return render(request, "item/form.html", {"form": form, "title": "Edit item"})


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect("/")


def items(request):
    query = request.GET.get("query", "")
    category_id = int(request.GET.get("category", 0))
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()
    if category_id:
        items = list(filter(lambda item: item.category.id == category_id, items))
        print(items)
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(
        request,
        "item/items.html",
        {
            "items": items,
            "query": query,
            "categories": categories,
            "category_id": category_id,
        },
    )
