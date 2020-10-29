from django.shortcuts import render, redirect
from . import util

from django.urls import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
import random
from django.contrib import messages

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_wiki(request, title):
    '''
        1. the view should be called by util entry function
        2. if entry which requested does'nt exist, it should indicate 404
        3. if exists, it should be presented
    '''
    content = util.get_entry(title)

    # Page not found
    if content is None:
        content = markdown2.markdown("#**404 page not found!**")
        return render(request, "encyclopedia/error.html", {
            "entries": content
        })

    return render(request, "encyclopedia/wiki.html", {
        "entries": markdown2.markdown(content),
        
        "title": title
    })

def search(request):
    '''
        type a query into the search box to search for an encyclopedia entry.

        1. If the query matches, the user should be redirected to that entry’s page.

        2. If the query does not match, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were Py, then Python should appear in the search results.

        3. Clicking on any of the entry names on the search results page should take the user to that entry’s page.
    '''
    # return HttpResponse(search_entry)
    # return HttpResponse(list_entries)  # CSSDjangoGitHTMLPython

    '''for entry in list_entries:   returns only CSS 
        return HttpResponse(entry)
    return render(request, "encyclopedia/search.html", {    returns ['CSS', 'Django', 'Git', 'HTML', 'Python']
        "results": list_entries
    })'''
    
    # get search_entry
    search_entry = request.POST['q']  # post
    # list of entries
    entry_list = util.list_entries()
    list_entries = []
    # convert all elements into lower
    for entries in entry_list:
        list_entries.append(entries.lower())

    content = util.get_entry(search_entry)

    if request.method == "POST":  # POSt
        # Checks in list entry, returns entry
        if search_entry.lower() in list_entries:
            return render(request, "encyclopedia/wiki.html", {
                "entries": markdown2.markdown(content),
                "title": search_entry #markdown2.markdown(f"#{search_entry}")
            })

        # Looks for substrings
        else:
            substrings = []
            for entry in list_entries:
                if search_entry.lower() in entry.lower():
                    substrings.append(entry.upper())

            # Page not found
            if not substrings:
                content = markdown2.markdown("#**404 page not found!**")
                return render(request, "encyclopedia/error.html", {
                    "entries": content
                })

            # Returns all substrings
            return render(request, "encyclopedia/search.html", {
                "substrings": substrings,
                "title": search_entry.upper()
            })

        '''
        for entry in list_entries:
            results.append(entry)
            if search_entry.upper() == entry.upper():
                return render(request, "encyclopedia/search.html", {
                    "results": markdown2.markdown(content),
                    "title": search_entry.upper()
                })
            else:
                #index(request)
                
                return render(request, "encyclopedia/search.html", {
                    "results": results,
                    'title': search_entry
                })

                #return render(request, "encyclopedia/index.html", {
                #    "entries": util.list_entries()
                #})
        '''

        '''
        if search_entry in list_entries:
            return HttpResponse(search_entry)
            # return HttpResponseRedirect("/wiki/" + request.POST["q"])
        else:
            for entry in list_entries:
                if search_entry in entry:
                    results.append(entry)
                    return render(request, "encyclopedia/search.html", {
                        "results": results
                    })
                else:
                    return HttpResponse("He")
        '''

# Form to input title name
class NewTitleForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control',
        'placeholder': 'Enter title of a page. (e.g. Python)'}))

# Form for textarea content
class NewTextArea(forms.Form):
    textarea = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10,
        'placeholder': 'Type content of a page in a markdown format.'}))

def create(request):
    '''
    Clicking “Create New Page” should take the user to a page where they can create a new entry.
    1. Users should be able to enter a title for the page and, in a textarea, should be able to enter the Markdown content for the page.
    2. Users should be able to click a button to save their new page.
    3. Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
    When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
    '''
    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        title_form = NewTitleForm(request.POST)
        textarea_form = NewTextArea(request.POST)

        # Check if form data is valid (server-side)
        if title_form.is_valid() and textarea_form.is_valid():

            # Isolate the title and textarea content from the 'cleaned' version of form data
            title = title_form.cleaned_data["title"]
            textarea = textarea_form.cleaned_data["textarea"]

            # Check if entry already exists
            if title in util.list_entries():
                content = markdown2.markdown("#**Title already exists try another one**")
                return render(request, "encyclopedia/wiki.html", {
                    "entries": content,
                    "title": title
                })

            # Save title and textarea content
            util.save_entry(title, textarea)
            # message
            messages.success(request, f"Entry named {title} has been created!")

            # Redirect user to list of entries
            return HttpResponseRedirect(reverse("index"))
            
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/create.html", {
                "titleForm": title_form
            })
    # if GET returns empty forms
    return render(request, "encyclopedia/create.html", {
        "titleForm": NewTitleForm(),
        "textareaForm": NewTextArea()
    })

# Edit page
def edit(request,title):
    
    # Content of an entry
    content = util.get_entry(title.strip())
    
    if request.method == 'POST':

        content = request.POST.get("content").strip()
        
        # Save title and textarea content
        util.save_entry(title, content)        

        # message
        messages.info(request, f"Entry named {title} has been edited!")

        # Redirect user to list of entries
        return redirect("get_wiki", title=title)
    
    else:

        return render(request, "encyclopedia/edit.html", {
            "pagename": title,
            "content": content
        })

# Random page
def randompage(request):

    # display a random page from list_entries    
    return get_wiki(request, random.choice(util.list_entries()))
