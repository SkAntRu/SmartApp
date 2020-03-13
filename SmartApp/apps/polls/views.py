from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from polls.models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, reverse('polls:results',
                                   kwargs={'question_id': question.id, }
                                   ))


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You did not select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return HttpResponseRedirect after successfully dealing with  POST data.
        # This prevents from being posted twice if a user hits the Back button
        return HttpResponseRedirect(reverse('polls:results',
                                            kwargs={'question_id': question.id, }
                                            ))
