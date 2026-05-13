from django.shortcuts import render, redirect

from . import util
import markdown 


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
    