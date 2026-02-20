from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from polls.models import Question


def index(request: HttpRequest) -> HttpResponse:
    latest_questions = Question.objects.order_by("-pub_date")[:5]

    return render(request, "polls/index.jinja", {"latest_questions": latest_questions})


def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "polls/detail.jinja", {"question": question})


def results(_request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"You're looking at the results of question {question_id}.")


def vote(_request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"You're voting on question {question_id}.")
