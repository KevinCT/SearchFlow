from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    return render(request, 'searchengine/query.html')

def query(request):
    if request.method == 'POST':
        query = request.POST.get('queryField', None)
        if query is not None:
            #Manipulate query here and return the search results.
            return HttpResponse(query)
        else:
            return HttpResponse("Search cannot be empty")
    else:
        return HttpResponse("Something went wrong")
