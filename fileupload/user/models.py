from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SiteUsers(models.Model):
    user =models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    position = models.CharField(max_length=20)
    email = models.CharField(max_length=100, null=True)
    program = models.CharField(max_length=180, null=True)
    pro_pic = models.ImageField(default="images/user-3.png",null=True, blank=True,upload_to='media')

class Question(models.Model):
    author = models.ForeignKey(User, null=True, on_delete = models.CASCADE)
    title = models.CharField(max_length = 300,null=False)
    subject = models.CharField(max_length=100, null=False)
    body = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title
    
    def get_responses(self):
        return self.responses.filter(parent=None)

class Response(models.Model):
    user = models.ForeignKey(User, null=False, on_delete = models.CASCADE)
    question = models.ForeignKey(Question, null=False, on_delete = models.CASCADE, related_name = 'responses')
    parent = models.ForeignKey('self', null=True, blank = True, on_delete = models.CASCADE)
    body = models.TextField(null = False)
    pdf = models.FileField( upload_to='media',blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.body
    
    def get_responses(self):
        return Response.object.filter(parent=self)


