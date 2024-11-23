from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text

class VoteUser(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    vote_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vote User'
        verbose_name_plural = 'Vote Users'
        unique_together = ['question', 'ip_address']

    def __str__(self):
        return f"{self.ip_address} - {self.question.question_text}"