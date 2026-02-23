import datetime
from typing import TYPE_CHECKING

from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from django.db.models import Manager


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name="date published")

    choice_set: Manager[Choice]

    def __str__(self) -> str:
        return self.question_text

    def was_published_recently(self) -> bool:
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    qustion_id: int

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.choice_text
