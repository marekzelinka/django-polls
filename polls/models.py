import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    class Meta:
        indexes = [models.Index(fields=["pub_date"])]

    id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name="date published")

    choices: models.Manager[Choice]

    def __str__(self) -> str:
        return self.question_text

    @admin.display(boolean=True, ordering="pub_date", description="Published recently?")
    def was_published_recently(self) -> bool:
        now = timezone.now()

        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    qustion_id: int
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )

    def __str__(self) -> str:
        return self.choice_text
