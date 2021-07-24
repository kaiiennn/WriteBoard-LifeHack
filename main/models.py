from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Module(models.Model):
    module = models.CharField(max_length=1000)

    def __str__(self):
        return self.module

    def get_absolute_url(self):
        return reverse('class-list', args=[str(self.id)])


class Class(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    Class = models.CharField(max_length=1000)

    def __str__(self):
        return self.Class

    def get_absolute_url(self):
        return reverse('lesson-list', args=[str(self.id)])


class Lessons(models.Model):
    Class = models.ForeignKey('Class', on_delete=models.CASCADE)
    lessonDateTime = models.DateTimeField()
    lesson = models.CharField(max_length=1000)

    def __str__(self):
        return self.lesson

    def get_absolute_url(self):
        return reverse('question-list', args=[str(self.id)])


class Question(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lesson = models.ForeignKey('Lessons', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_responses(self):
        return self.responses.filter(parent=None)

    def get_absolute_url(self):
        return reverse('question', args=[str(self.id)])


class Response(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, null=False, on_delete=models.CASCADE, related_name='responses')
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

    def get_responses(self):
        return Response.objects.filter(parent=self)
