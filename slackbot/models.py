from django.db import models
from django.utils import timezone

class Slackuser(models.Model):
    username = models.TextField()
    last_reminder = models.DateTimeField(default=timezone.now)
    last_private_nag = models.DateTimeField(default=timezone.now)
    last_public_nag = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'slackbot'

class Message(models.Model):
    channel = models.TextField()
    text = models.TextField(max_length=500)
    dt = models.DateTimeField()
    slackuser = models.ForeignKey(Slackuser, on_delete=models.CASCADE)

    class Meta:
        app_label = 'slackbot'
