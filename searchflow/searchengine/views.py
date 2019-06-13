import os
import pickle
import time

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import loader

from crawler.extrafunctions import *  # remove SearchFlow
from crawler.mongodb import Connection
from indexing.indexing import create_dictionary as cd


# Create your views here.

def index(request):
    topTags = getTags()
    template = loader.get_template('index.html')
    context = {
        'tag_list': topTags,

    }
    return HttpResponse(template.render(context, request))


def question_view(request):
    doc = request.GET.get('questionSubmit', None)
    doc = str(doc).split("/")[-1:]
    data = Connection(db_name="StackOverflow", db_col="final_processed_data_without_code").get_data_with_value(
        data_type="Question.question_id", value=int(doc[0].strip()))
    question_text = (data.get("Question").get("question_text"))
    question_title = data.get("Question").get("question_title")
    question_code = data.get("Question").get("question_code")
    question_related = data.get("Question").get("related_questions")
    questionList = [(question_title, question_text, question_code)]
    related_question_list = []
    for question in question_related:
        related_question_list.append(("https://stackoverflow.com/questions/" + str(question.get('related_question_id')),
                                      question.get('related_question')))
    all_answers = []
    for x in data["Answer"].get("answers"):
        all_answers.append(x.get('answer'))
    template = loader.get_template('page.html')
    context = {
        'answer_list': all_answers,
        'question_list': questionList,
        'related_question_list': related_question_list,

    }
    return HttpResponse(template.render(context, request))

def query(request):
    start_time = time.time()
    if request.method == 'GET':
        topTags = getTags()
        query = request.GET.get('queryField', None)
        query = str(query).lower()

        option = request.GET.get('optionSelector', None)
        if option == "classifier":
            option = predict_title_code(query)
            option = str(option).lower()

        tags = [request.GET.get('tOne'), request.GET.get('tTwo'), request.GET.get('tThree'), request.GET.get('tFour'),
                request.GET.get('tFive')]
        tags = list(filter(None, tags))
        if option == 'tag':
            for tag in tags:
                query = query + tag

        if query == '':
            template = loader.get_template('index.html')
            context = {
                'tag_list': topTags,
            }
            return HttpResponse(template.render(context, request))



        insertTop(query)  # inserting the query terms in the db, helps to find a top searched term
        # tags is a list of tags, option is the way the result should be sorted(e.g. by answer, question, date..)
        # method for returning data from backend required here. getData(query, tags, option) should return a list of tuples which contains (title, link, description)

        docs = 20
        results = cd.get_search(query, docs, region=option)
        resultList = []
        doc = results.get()
        for x in range(0, docs):
            sentence_text, start_pos, end_pos = get_sentence(str(doc[2].get("Question").get("question_text")),
                                                             query.split())

            resultList.append((doc[2].get("Question").get("question_title"),
                               "https://stackoverflow.com/questions/" + str(doc[2].get("Question").get("question_id")),
                               sentence_text, start_pos, end_pos))
            if results.empty() is False:
                doc = results.get(False)
        template = loader.get_template('results.html')
        final_time = time.time() - start_time
        print("Time: ", final_time)

        save_result_list = []
        for r in resultList:
            save_result_list.append(r[1])
        save_to_excel_performance(save_result_list, query, option, final_time, flag=False)

        paginator = Paginator(resultList, docs)
        page = request.GET.get('page')
        result = paginator.get_page(page)
        context = {
            'result': result,
            'tag_list': topTags,
            'query_list': [query],

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


def predict_title_code(data):
    print(os.getcwd())
    loaded_model = pickle.load(open(os.getcwd() + "\\searchengine\\finalized_model.sav", 'rb'))
    data = [data]
    result = loaded_model.predict(data)
    return result[0]
