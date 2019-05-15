from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.templatetags.static import static
import json
from searchengine.scoring import *
# Create your views here.

def index(request):
    return render(request, 'index.html')

def query(request):
#    with open(static('searchengine/style.css'), encoding="utf8") as f:
#        data = [json.loads(line) for line in f]
    if request.method == 'GET':
        query = request.GET.get('queryField', None)
        if query is not None:
            #method for returning data from backend. getData(query) should return a list of list which contains [title, link, description]
            resultList = [['dummy data', "test"]]
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
