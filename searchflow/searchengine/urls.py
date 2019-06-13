from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query', views.query, name = 'query'),
    path('question_view', views.question_view, name='question_view'),

]
