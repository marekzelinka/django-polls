from typing import TYPE_CHECKING

from django.db.models import F
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from polls.models import Choice, Question

if TYPE_CHECKING:
    from django.db.models import BaseManager


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions_list"

    def get_queryset(self) -> BaseManager[Question]:
        """Returns the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except KeyError, Choice.DoesNotExist:
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice."},
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
