from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question
from django.template import loader

def index(request):
    last_question_list = Question.objects.order_by('-pub_date')[0:5]
    # template = loader.get_template('polls/index.html')  # 载入index.html文件
    context = {
        'last_question_list': last_question_list,
    }
    # output = ','.join([q.question_text for q in last_question_list])
    # return HttpResponse(output)
    # return HttpResponse(template.render(context, request))  # 更简洁的方式如下,不需要loader template
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # 如果题号不存在，则显示404
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist.')
    # 上述代码可以直接使用get_object_or_404()代替
    question = get_object_or_404(Question, pk=question_id)
    # return HttpResponse('You are looking at question %s.'%question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = 'You are looking at the resutls of question %s.'
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse('You are voting at question %s.' % question_id)