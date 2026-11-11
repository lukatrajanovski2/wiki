from django.shortcuts import render
import markdown2
from . import util
import os
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

class NewTaskForm(forms.Form):
    title = forms.CharField(label="title")
    body = forms.CharField(label="body")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Оваа статија не постои!"
        })
    html_content = markdown2.markdown(content)
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

def search(request):
    query = request.GET.get("q", "")
    results = []
    storage_data = "entries"
    if os.path.exists(storage_data):
        all_files = os.listdir(storage_data)
        for filename in all_files:
            if filename.endswith(".md"):
                title = filename.replace(".md", "")
                if query.lower() in title.lower():
                   results.append(title)
            else:
                if filename.endswith(".md"):
                        title = filename.replace(".md", "")
                        results+=title
    return render(request, "encyclopedia/index.html",{
        "query":query,
        "entries":results
    })

def create(request):
    if request.method == "POST":
        valid = NewTaskForm(request.POST)
        if valid.is_valid():
            title = valid.cleaned_data["title"]
            body = valid.cleaned_data["body"]
            util.save_entry(title, body)
            return HttpResponseRedirect(reverse("entry", args=[title]))
    return render(request, "encyclopedia/create.html", {
      "valid":NewTaskForm()  
    })

def random_page(request):
    if request.method == "GET":
        post = util.list_entries()
        random_page = random.choice(post)
        return HttpResponseRedirect(reverse("entry", args=[random_page]))