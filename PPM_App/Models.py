from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')

    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    poll = models.ForeignKey(Poll, related_name='responses', on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice, related_name='responses')

    def __str__(self):
        return f'{self.user} responded to {self.poll}'
