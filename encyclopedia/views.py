from turtle import title

from django.shortcuts import render, redirect
from django import forms
from . import util
import markdown 
import random


class NewTaskForm(forms.Form):
    task = forms.CharField(label="Title")
    content = forms.CharField(label="content", widget=forms.Textarea)      


def index(request):
    """
    View function for the index page, which lists all encyclopedia entries.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    """
    View function for an encyclopedia entry.
    """
    # get the entry content from the util module
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "title": "Page Not Found",
            "message": "The requested page was not found."
        })
    
    # convert markdown content to HTML
    html_content = markdown.markdown(entry)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    """
    View function for handling search queries.
    """
    query = request.GET.get("q", "")
    entries = util.list_entries()

    # check for exact match first
    for entry in entries:
        if entry.lower() == query.lower():
            return redirect("entry", title=entry)
        
    # if no exact match, find entries that contain the query as a substring
    results = [entry for entry in entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": results
            })

def new_page(request):
    """
    View function for creating a new encyclopedia entry.
    """
    # if the request method is POST, process the form data
    if request.method == "POST":
        form = NewTaskForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["task"]
            content = form.cleaned_data["content"]

            # check if an entry with the same title already exists
            if util.get_entry(title) is not None:
                 return render(request, "encyclopedia/error.html", {
                    "title": "Error",
                    "message": "An entry with that title already exists."
            }) 

    
            # if the title is unique, save the new entry and redirect to its page
            util.save_entry(title, content)
            
        
            # Redirect to the new entry page
            return redirect("encyclopedia:entry", title=title)
        

    # if the request method is GET, display the form
        else:
            return render(request, "encyclopedia/new_page.html", {
            "form": form 
        })

    return render(request, "encyclopedia/new_page.html", {
        "form": NewTaskForm()
    })



def edit(request, title):
    """
    View function for editing an existing encyclopedia entry.
    """

    # Get an existing encyclopedia entry content.
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "title": "Page Not Found",
            "message": "The requested page was not found"
        
        })
    
    # If the request method is POST, process the data
    if request.method == "POST":
        form = NewTaskForm(request.POST)

        if form.is_valid():
            new_title = form.cleaned_data["task"]
            new_content = form.cleaned_data["content"]



            # Check if the updated title already exists
            if new_title != title and util.get_entry(new_title) is not None:
                return render (request, "encyclopedia/error.html", { 
                    "title": "Error",
                    "message": "An entry with the same title already exists"
                })
        
            # Save updated entry content
            util.save_entry(new_title, new_content)

            return redirect("encyclopedia:entry", title=new_title)
        
    else:
        # Handle GET request (pre-populate form)
        form = NewTaskForm(initial={
            "task": title,
            "content": entry
        })

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })



def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect ('encyclopedia:entry', title=random_entry)

    







    
