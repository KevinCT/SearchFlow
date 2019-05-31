from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from crawler.extrafunctions import *
# Create your views here.

def index(request):
    backupList = ["java", "python", "c++", "javascript", "android" ]
    topTags = topSearch()
    if len(topTags) >= 5:
        topTags = [tuple(topTags[:5])]
    else:
        length = len(topTags)
        for i in range(length, 5):
            topTags.append(backupList[i])
        topTags = [tuple(topTags[:5])]
    template = loader.get_template('index.html')
    print(topTags)
    context = {
        'tag_list': topTags
    }
    return HttpResponse(template.render(context, request))


def query(request):
    if request.method == 'GET':
        query = request.GET.get('queryField', None)
        option = request.GET.get('optionSelector', None)
        if query is not None:
            insertTop(query)
            #method for returning data from backend. getData(query) should return a list of tuples which contains (title, link, description)
            resultList = [(query + option, "http://www.stackoverflow.com", "This page shows how to remove the hyperlink underline with CSS by using the text-decoration property. Did you know that removing the underline allows you to ...")]
            template = loader.get_template('results.html')
            context = {
                'result_list': resultList,
            }
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse("Search cannot be empty")
    else:
        return HttpResponse("Something went wrong")
