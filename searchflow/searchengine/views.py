from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from crawler.extrafunctions import *
# Create your views here.

def index(request):
    return render(request, 'index.html')

def query(request):
    if request.method == 'GET':
        query = request.GET.get('queryField', None)
        if query is not None:
            insertTop(query)
            #method for returning data from backend. getData(query) should return a list of tuples which contains (title, link, description)
            resultList = [(query, "http://www.stackoverflow.com", "This page shows how to remove the hyperlink underline with CSS by using the text-decoration property. Did you know that removing the underline allows you to ...")]
            template = loader.get_template('results.html')
            #Manipulate query here and return the search results.
            context = {
                'latest_question_list': resultList,
            }
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse("Search cannot be empty")
    else:
        return HttpResponse("Something went wrong")
