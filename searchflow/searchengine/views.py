from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from crawler.extrafunctions import * #remove SearchFlow
from django.core.paginator import Paginator
from django.shortcuts import render
from indexing.indexing import create_dictionary as cd
import re


# Create your views here.

def index(request):
    fullTags = ["Java", "Python", "Android"]
    topTags = getTags()
    template = loader.get_template('index.html')
    context = {
        'tag_list': topTags,
        'full_tag_list': fullTags,

    }
    return HttpResponse(template.render(context, request))


def query(request):
    if request.method == 'GET':
        fullTags = ["Java", "Python", "Android"]
        topTags = getTags()
        query = request.GET.get('queryField', None)
        option = request.GET.get('optionSelector', None)
        tags = [request.GET.get('tOne'), request.GET.get('tTwo'), request.GET.get('tThree'), request.GET.get('tFour'),
                request.GET.get('tFive')]
        tags = list(filter(None, tags))
        tags2 = request.GET.get('tagInput')
        tags2 = tags2.split(',')
        tags = tags + tags2
        print(tags)

        insertTop(query)
        #tags is a list of tags, option is the way the result should be sorted(e.g. by answer, question, date..)
        #method for returning data from backend required here. getData(query, tags, option) should return a list of tuples which contains (title, link, description)
        docs = 100
        results = cd.get_search(query, docs)

        resultList = []
        doc = results.get()
        for x in range(0, docs):
            resultList.append((doc[2].get("Question").get("question_title"), "https://stackoverflow.com/questions/" + str(doc[2].get("Question").get("question_id")), ""))
            if results.empty() is False:
                doc = results.get(False)
        resultListBlock = [resultList[i * 10:(i + 1) * 10] for i in range((len(resultList) + 10 - 1) // 10)]
        template = loader.get_template('results.html')

        paginator = Paginator(resultList, docs)
        page = request.GET.get('page')
        users = paginator.get_page(page)
        context = {
            'users': users,
            'tag_list': topTags,
            'full_tag_list': fullTags,

        }
        return HttpResponse(template.render(context, request))

    else:
        return HttpResponse("Something went wrong")

#            return listing(request, resultList)


#def listing(request, resultList):
#    paginator = Paginator(resultList, 10)
#    page = request.GET.get('page')
#    users = paginator.get_page(page)
#    return render(request, 'results.html', {'users': users})

def getTags():
    backupList = ["java", "python", "c++", "javascript", "android" ]
    topTags = topSearch()
    if len(topTags) >= 5:
        topTags = [tuple(topTags[:5])]
    else:
        length = len(topTags)
        for i in range(length, 5):
            topTags.append(backupList[i])
        topTags = [tuple(topTags[:5])]
    return topTags
