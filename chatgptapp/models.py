from django.db import models

# Create your models here.

class Tbl_User(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class Tbl_QuestionAnswer(models.Model):
    question = models.CharField(max_length=100,default='')
    answer = models.CharField(max_length=800,default='')
    status = models.CharField(max_length=100,default='')
    user=models.ForeignKey(Tbl_User,on_delete=models.CASCADE,default='')

# class ChatLog(models.Model):
#     user_message = models.TextField()
#     bot_response = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

