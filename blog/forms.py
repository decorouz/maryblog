# Core Django imports
from curses import meta
from dataclasses import field, fields
from django.db import models
from django.forms import ModelForm, TextInput, EmailInput, Textarea

from django import forms

# Blog application imports
from blog.models import Comment, Post

# Third-party app imports
from ckeditor.widgets import CKEditorWidget


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=100)
    sender_email = forms.EmailField()
    receiver_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(ModelForm):
    """Creating form from Comment model"""
    class Meta:
        model = Comment
        fields = ("name", "email", "body")

        widgets = {
            "name": TextInput(attrs={"aria-required": "true",
                                     "name": "contact-form-name",
                                     "class": "form-control",
                                     "placeholder": "Enter your name",
                                     "aria-valid": "true"}),

            "email": EmailInput(attrs={"aria-required": "true",
                                       "name": "contact-form-email",
                                       "class": "form-control",
                                       "placeholder": "Enter your email",
                                       "aria-valid": "true"}),

            "body": Textarea(attrs={"row": 2,
                                    "name": "contact-form-message",
                                    "class": "text-area-message form-control",
                                    "placeholder": "Enter your comment",
                                    "arai-required": "true",
                                    "aria-valid": "false"})
        }


class SearchForm(forms.Form):
    query = forms.CharField()


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "featured_image",
                  "body", "status", "tags"]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
