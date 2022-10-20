from operator import mod
from statistics import mode
from django.db import models

# Create your models here.
CATAGORIES = (
('nature','nature'),('travel','travel'),('animal','animal')
)
class Blog(models.Model):
    name=models.CharField(max_length=500)
    desc = models.CharField(max_length=2000)
    image1 = models.FileField(upload_to='static/uploads')
    catagory = models.CharField(max_length=20 , choices=CATAGORIES)

class Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE, null=True)
    text =  models.CharField(max_length=500)
    parent = models.ForeignKey('self', on_delete=models.CASCADE , null=True)

class Replycomment(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE, null=True)
    text =  models.CharField(max_length=500)

class LikeBlog(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE, null=True)
    like = models.IntegerField()
