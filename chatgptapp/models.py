from django.db import models
from django.contrib.auth.models import User


    
class QuestionAnswer(models.Model):
    question = models.TextField()
    answer = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"Question: {self.question}, Answer: {self.answer}"

    class Meta:
        db_table = 'QuestionAnswer'
