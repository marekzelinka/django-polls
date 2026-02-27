from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self) -> None:
        """
        `was_published_recently()` returns `False` for questions whose `pub_date`
        is in the future.
        """
        time = timezone.now() + timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self) -> None:
        """
        `was_published_recently()` returns `False` for questions whose `pub_date` is
        older than 1 day.
        """
        time = timezone.now() - timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self) -> None:
        """
        `was_published_recently()` returns `True` for questions whose `pub_date` is
        within the last day.
        """
        time = timezone.now() - timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)


def create_question(*, question_text: str, days: float) -> Question:
    """
    Create a question with the given `question_text` and published the given number of
    `days` offset to now (negative for questions published in the past, positive for
    questions that have yet to be published).
    """
    pub_date = timezone.now() + timedelta(days=days)

    return Question.objects.create(question_text=question_text, pub_date=pub_date)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self) -> None:
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response=response, text="No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self) -> None:
        """
        Questions with a pub_date in the past are displayed on the index page.
        """
        past_question = create_question(question_text="Past Question", days=-30)

        response = self.client.get(reverse("polls:index"))

        self.assertContains(response=response, text=past_question.question_text)
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_future_question(self) -> None:
        """
        Questions with a pub_date in the future aren't displayed on the index page.
        """
        future_question = create_question(question_text="Future Question", days=30)

        response = self.client.get(reverse("polls:index"))

        self.assertContains(response=response, text="No polls are available.")
        self.assertNotContains(response=response, text=future_question.question_text)
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_and_past_questions(self) -> None:
        """
        Even if both past and future questions exist, only past questions are displayed
        on the index page.
        """
        past_question = create_question(question_text="Past Question", days=-30)
        future_question = create_question(question_text="Future Question", days=30)

        response = self.client.get(reverse("polls:index"))

        self.assertNotContains(response=response, text="No polls are available.")
        self.assertNotContains(response=response, text=future_question.question_text)
        self.assertContains(response=response, text=past_question.question_text)
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_two_past_questions(self) -> None:
        """
        The questions index page may display multiple questions.
        """
        first_question = create_question(question_text="Past Question 1", days=-30)
        latest_question = create_question(question_text="Past Question 2", days=-5)

        response = self.client.get(reverse("polls:index"))

        self.assertQuerySetEqual(
            response.context["latest_question_list"], [latest_question, first_question]
        )
