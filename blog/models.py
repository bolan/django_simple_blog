import datetime
import os.path
from django.utils import timezone
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

class Category(models.Model):
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField("Added date")
    flat = models.BooleanField("Flat Category")

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    pub_date = models.DateTimeField("posted date")
    content = models.TextField()

    def __unicode__(self):
        return self.title

class Attachment(models.Model):
    attachments = models.FileField(upload_to='attachments/%Y/%m/%d/', max_length=100, blank=True)
    article = models.ForeignKey(Article,)
    
    def filename(self):
        return os.path.basename(self.attachments.name)

class Comment(models.Model):
    name = models.CharField("Your name", max_length=100)
    comment = models.TextField("Your Comment")
    pub_date = models.DateTimeField("Posted date", auto_now=False, auto_now_add=True)
    article = models.ForeignKey(Article)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
