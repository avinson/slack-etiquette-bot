from django.db import models

class User(models.Model):
    username = models.TextField()

    class Meta:
        app_label = 'slackbot'

class Message(models.Model):
    channel = models.TextField()
    text = models.TextField(max_length=500)
    ts = models.TextField()
    user = models.ForeignKey(User)

    class Meta:
        app_label = 'slackbot'
