from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# def index(request):
#     last_question_list = Question.objects.order_by('-pub_date')[0:5]
#     # template = loader.get_template('polls/index.html')  # 载入index.html文件
#     context = {
#         'last_question_list': last_question_list,
#     }
#     # output = ','.join([q.question_text for q in last_question_list])
#     # return HttpResponse(output)
#     # return HttpResponse(template.render(context, request))  # 更简洁的方式如下,不需要loader template
#     return render(request, 'polls/index.html', context)
#
# def detail(request, question_id):
#     # 如果题号不存在，则显示404
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404('Question does not exist.')
#     # 上述代码可以直接使用get_object_or_404()代替
#     question = get_object_or_404(Question, pk=question_id)
#     # return HttpResponse('You are looking at question %s.'%question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     # response = 'You are looking at the resutls of question %s.'
#     # return HttpResponse(response % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


# 将上面的代码改成通用文档视图
class IndexView(generic.ListView):
    # ListView 对应于显示一个对象列表
    template_name = 'polls/index.html'
    context_object_name = 'last_question_list'
    def get_queryset(self):
        """Return the last five published questions.
        (not including those set to be published in the future)"""
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    # DetailView 对应于显示一个特定类型对象的详细信息
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """不显示哪些出版日期在未来某天的信息"""
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    # return HttpResponse('You are voting at question %s.' % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 如果出现error，则显示问题的投票表单
        return render(request, 'polls/detail.html', {'question': question,
                                                     'error_message': "You didn't select a choice.",
                                                     })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 表单数据提交后，永远要加一个HttpResponseRedirct,防止用户点击back之后将表单提交两次
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))