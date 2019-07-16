from django.db import models

class User(models.Model):
    username = models.TextField()

class Message(models.Model):
    channel = models.TextField()
    text = models.TextField()
    ts = ??
    user = models.ForeignKey(User)
