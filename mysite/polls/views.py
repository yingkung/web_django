from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello, world! You are at the polls index.')


def detail(request, question_id):
    return HttpResponse('You are looking at question %s.'%question_id)


def results(request, question_id):
    response = 'You are looking at the resutls of question %s.'
    return HttpResponse(response% question_id)


def vote(request, question_id):
    return HttpResponse('You are voting at question %s.' % question_id)