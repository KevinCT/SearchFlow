from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from crawler.extrafunctions import *
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

def index(request):
    topTags = getTags()
    template = loader.get_template('index.html')
    context = {
        'tag_list': topTags
    }
    return HttpResponse(template.render(context, request))


def query(request):
    if request.method == 'GET':
        topTags = getTags()
        query = request.GET.get('queryField', None)
        option = request.GET.get('optionSelector', None)
        tags = [request.GET.get('tOne'), request.GET.get('tTwo'), request.GET.get('tThree'), request.GET.get('tFour'),
                request.GET.get('tFive')]
        tags = list(filter(None, tags))

        insertTop(query)
        #tags is a list of tags, option is the way the result should be sorted(e.g. by answer, question, date..)
        #method for returning data from backend required here. getData(query, tags, option) should return a list of tuples which contains (title, link, description)



        resultList = []
        for i in range (0, 40):
          resultList.append((query + option + str(i), "http://www.stackoverflow.com", "This page shows how to remove the hyperlink underline with CSS by using the text-decoration property. Did you know that removing the underline allows you to ..."))
    #    resultListBlock = [resultList[i * 10:(i + 1) * 10] for i in range((len(resultList) + 10 - 1) // 10)]
        template = loader.get_template('results.html')

        paginator = Paginator(resultList, 10)
        page = request.GET.get('page')
        users = paginator.get_page(page)
        context = {
            'users': users,
            'tag_list': topTags,
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
