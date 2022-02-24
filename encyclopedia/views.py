from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django import forms
from . import util
from .forms import SearchForm, EntryForm
from .models import EntryModel, SearchModel
from random import choice
import markdown2
from markdown2 import Markdown
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def index(request):
    formS = SearchForm()
    entries = util.list_entries() #Call appropriate util.py function to get list of all entries
    return render(request, "encyclopedia/index.html", {
    "formS": SearchForm(),
    "entries": entries
    })


def entry(request, title):
    formS = SearchForm()
    ent = util.get_entry(f"{title}") #Call appropriate util.py function to get entry by title name
    if ent is not None:
        html = markdown2.markdown(ent)  #Convert markdown content to hmtl
        return render(request, "encyclopedia/entryfile.html", {"title": title, "html": html, "formS": SearchForm()})
    else:
        return HttpResponse(status=404)


def search(request):
    title_list = util.list_entries()
    title = request.GET['title']
    if default_storage.exists(f"entries/{title}.md"):
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=(title, )))
    else:
        formS = SearchForm()
        entries = [i for i in title_list if title in i]
        return render(request, "encyclopedia/index.html", {
        "formS": SearchForm(),
        "entries": entries
        })


def newpage(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        formS = SearchForm()
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if default_storage.exists(f"entries/{title}.md"):
                return render(request, "encyclopedia/newpage.html", {
                "form": form,
                "formS": SearchForm(),
                "error": "Filename already exists, choose a different name."
                })
            else:
                util.save_entry(title, content)
                html =  markdown2.markdown(content) #Convert markdown content to hmtl
                return render(request, f"encyclopedia/entryfile.html", {
                "title": title,
                "html": html,
                "form": EntryForm(),
                "formS": SearchForm()
            })
        else:
            return render(request, "encyclopedia/newpage.html", {
            "form": form,
            "formS": SearchForm()
            })
    else:
        return render(request, "encyclopedia/newpage.html", {
        "form": EntryForm(),
        "formS": SearchForm()
        })


def editentry(request, title):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        formS = SearchForm()
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)     #Call appropriate util.py function to save entry.
            ent = util.get_entry(f"{title}")    #Call appropriate util.py function to get entry by title name.
            html =  markdown2.markdown(content)  #Convert markdown content to hmtl
            return render(request, f"encyclopedia/entryfile.html", {
            "title": title,
            "html": html,
            "formS": SearchForm()
            })
    else:
        ent = util.get_entry(f"{title}")  #Call appropriate util.py function to get entry by title name
        content = ent
        data = {'title': title,
                'content': content}
        form = EntryForm(data)
        return render(request, f"encyclopedia/editpage.html", {
        "form": form,
        "data": data,
        "title": title,
        "formS": SearchForm()
        })


def randompage(request):
    return entry(request, choice( util.list_entries()))
