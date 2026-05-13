from django.shortcuts import render

from . import util
import markdown 


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "title": "Page Not Found",
            "message": "The requested page was not found."
        })
    html_content = markdown.markdown(entry)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })
    

