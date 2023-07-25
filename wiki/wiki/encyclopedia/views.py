from django import template
from markdown2 import Markdown
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# shows new page entry
def entry(request, name):
    name = name.lower()
    if util.get_entry(name) is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry_name": name,
            "content": convert_markdown_to_html(util.get_entry(name))
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Sorry, no entry found."
        })

# search for an entry
def search(request):
    if request.method == "POST":
        entry_search = request.POST["q"]
        html_content = convert_markdown_to_html(util.get_entry(entry_search))
        # render the entry page if search exists
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
            "tite": entry_search,
            "content": html_content
            })
        else:
            # print similar search results if search doesn't exist
            currEntries = util.list_entries()
            results = []
            for entry in currEntries:
                # search for similar entry using substrings
                if entry_search.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "search_results": results
            })

    

# converts markdown to HTML with markdown library
def convert_markdown_to_html(content):
    markdowner = Markdown()
    if content is not None:
        return markdowner.convert(content)
    else:
        return None


# allows the user to create a new entry
def new(request):
    if request.method == "GET":
        return render(
            request,
            "encyclopedia/new.html"
        )
    else: 
        title = request.POST["title"]
        content = request.POST["content"]
        html_content = convert_markdown_to_html(util.get_entry(title))
        # check if entry already exists
        if html_content is not None:
             return render(request, "encyclopedia/error.html", {
            "message": "Sorry, entry already exists."
            })  
        else: 
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
            "tite": title,
            "content": convert_markdown_to_html(content)
            })
           


# returns a random entry
def rand(request):
    currEntries = util.list_entries()
    rand_entry = random.choice(currEntries)
    html_content = convert_markdown_to_html(util.get_entry(rand_entry))
    return render(request, "encyclopedia/entry.html", {
            "title": rand_entry,
            "content": html_content
            })


# allows the user to edit an entry
def edit(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        content = util.get_entry(entry_search)
        return render(
            request,
            "encyclopedia/edit.html", {
                "entry_title": entry_search,
                "content": content
            }
        )
    
# save edits
def save(request):
    if request.method == "POST":
        entry_search = request.POST['title']
        content = convert_markdown_to_html(request.POST['content'])
        util.save_entry(entry_search, content)
        return render(
            request,"encyclopedia/entry.html", {
            "title": entry_search,
            "content": content
            })
