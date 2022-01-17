# Core Django imports
from django.forms import ModelForm, TextInput, EmailInput, Textarea
from django import forms

# Blog application imports
from blog.models import Comment


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
                                    "placeholder": "Enter your email",
                                    "arai-required": "true",
                                    "aria-valid": "false"})
        }


class SearchForm(forms.Form):
    query = forms.CharField()


#
