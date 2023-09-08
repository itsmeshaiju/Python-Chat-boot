from django.db import models

# Create your models here.

class Tbl_User(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class Tbl_QuestionAnswer(models.Model):
    question = models.TextField()
    answer = models.TextField()
    user=models.ForeignKey(Tbl_User,on_delete=models.CASCADE,default='')
    timestamp = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"Question: {self.question}, Answer: {self.answer}"
