from django.db import models

# Create your models here.

class Tbl_QuestionAnswer(models.Model):
    question = models.CharField(max_length=100,default='')
    answer = models.CharField(max_length=800,default='')
    status = models.CharField(max_length=100,default='')

class ChatLog(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)