from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
#function to get the page for the title given by the user
def view_entry(request,title):
    html_file = html_conv(title) # checking if the page exists or not using the function html_conv
    if html_file == None:
        return render(request,"encyclopedia/error.html",{
            "output" : "Error. Page does not exist.", # passing an error message to the page
            "title" : title
        })
    else:
        return render(request,"encyclopedia/entry_page.html",{ # to send the title and html content from backend to frontend
            "title" : title, # we define the title variable
            "html_file" : html_file # and the ntml file to be used in the page
        })
        
        
def search(request):
    #checking if the method is post
    if request.method == "POST":
        search_ip = request.POST['q']
        html_file = html_conv(search_ip)
        if html_file is not None:
            return render(request,"encyclopedia/entry_page.html",{
                "title" : search_ip,
                "html_file" : html_file
            })
        else:
            entries = util.list_entries()
            search_results = []
            for entry in entries:
                if search_ip.lower() in entry.lower():
                    search_results.append(entry)
            return render(request,"encyclopedia/search_result.html",{
                "search_results":search_results,
            })
            
def newpage(request):
    if request.method == "GET":
        return render(request,"encyclopedia/newpage.html")
    else:
        title = request.POST['title']
        print(f"This is the title entered by the user : {title}")
        content = request.POST['content']
        print(f"This is the content entered by the user : {content}")
        present_title = util.get_entry(title) #will return if the title is present in the current list or not
        if present_title is not None: # checking if the title is present 
            return render(request,"encyclopedia/error.html",{
                "output" : "The title already exists.",
                "title" : title
            })
        else: # here we will have to save entry to the entries folder
            util.save_entry(title,content)
            html_file = html_conv(title)
            return render(request,"encyclopedia/entry_page.html",{
                "title" : title,
                "html_file" : html_file
            })
#function to let the user edit the page and the markdown content should already be present in the textarea     
def edit_page(request):
    if request.method == "POST":
        title = request.POST['title_ip'] # we take in the title from the form placed in the entry page
        content = util.get_entry(title)
        return render(request,"encyclopedia/edit_page.html",{
            "title":title,
            "content" : content
        })
        
def save(request):
    if request.method =="POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_file = html_conv(title)        
        return render(request,"encyclopedia/entry_page.html",{
            "title":title,
            "html_file": html_file
        })

def random_page(request):
    entries = util.list_entries()
    rd_page = random.choice(entries)
    #now we have to convert the entry into HTML
    html_file = html_conv(rd_page)
    return render(request,"encyclopedia/entry_page.html",{
        "title" : rd_page,
        "html_file":html_file
        
    })


#converting Markdown content to HTML, input taken will be the title of the md file
def html_conv(title):
    md_file = util.get_entry(title)
    markdowner = Markdown()
    if md_file == None: #checking if the file exists, this variable should contain the 
        return None
    else:
        return markdowner.convert(md_file)
