import time

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import loader

from crawler.extrafunctions import *  # remove SearchFlow
from indexing.indexing import create_dictionary as cd


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


def question_view(request):
    print("test")
    template = loader.get_template('page.html')
    context = {
        'answer_list': [('test', 'test', 'test')]

    }
    return HttpResponse(template.render(context, request))
def query(request):
    start_time = time.time()
    if request.method == 'GET':
        fullTags = ["Java", "Python", "Android"]
        topTags = getTags()
        query = request.GET.get('queryField', None)
        query = str(query).lower()
        option = request.GET.get('optionSelector', None)
        tags = [request.GET.get('tOne'), request.GET.get('tTwo'), request.GET.get('tThree'), request.GET.get('tFour'),
                request.GET.get('tFive')]
        tags = list(filter(None, tags))
        tags2 = request.GET.get('tagInput')
        tags2 = tags2.split(',')
        tags = tags + tags2
        #        print(tags)

        insertTop(query)  # inserting the query terms in the db, helps to find a top searched term
        # tags is a list of tags, option is the way the result should be sorted(e.g. by answer, question, date..)
        # method for returning data from backend required here. getData(query, tags, option) should return a list of tuples which contains (title, link, description)

        docs = 20
        results = cd.get_search(query, docs, region=option)
        resultList = []
        doc = results.get()
        for x in range(0, docs):
            print(query.split())
            sentance_text, start_pos, end_pos = get_sentence(str(doc[2].get("Question").get("question_text")),
                                                             query.split())

            resultList.append((doc[2].get("Question").get("question_title"),
                               "https://stackoverflow.com/questions/" + str(doc[2].get("Question").get("question_id")),
                               sentance_text, start_pos, end_pos))
            if results.empty() is False:
                doc = results.get(False)
        # resultListBlock = [resultList[i * 10:(i + 1) * 10] for i in range((len(resultList) + 10 - 1) // 10)]
        template = loader.get_template('results.html')
        final_time = time.time() - start_time
        print("Time: ", final_time)
        save_result_list = []
        for r in resultList:
            save_result_list.append(r[1])
        save_to_excel_performance(save_result_list, query, option, final_time, flag=False)
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


def getTags():
    backupList = ["java", "python", "c++", "javascript", "android"]
    topTags = topSearch()
    if len(topTags) >= 5:
        topTags = [tuple(topTags[:5])]
    else:
        length = len(topTags)
        for i in range(length, 5):
            topTags.append(backupList[i])
        topTags = [tuple(topTags[:5])]
    return topTags


def get_sentence(text, phrase):
    for x in phrase:
        if x in text:
            index = str(text).index(x)
            end = index + len(x) + min(len(text), 50)
            if (index - 60) < 0:
                start = 0
            else:
                start = index - 50
            return text[start:end], index, index + len(x)
    return "", 0, 0
