from django.db.models import F
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from polls.models import Choice, Question


def index(request: HttpRequest) -> HttpResponse:
    latest_questions = Question.objects.order_by("-pub_date")[:5]

    return render(
        request, "polls/index.dj.html", {"latest_questions": latest_questions}
    )


def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "polls/detail.dj.html", {"question": question})


def results(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "polls/results.dj.html", {"question": question})


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except KeyError, Choice.DoesNotExist:
        return render(
            request,
            "polls/detail.dj.html",
            {"question": question, "error_message": "You didn't select a choice."},
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
