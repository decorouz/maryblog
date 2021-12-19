from django import forms

from blog.models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=100)
    sender_email = forms.EmailField()
    receiver_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """Creating form from Comment model"""
    class Meta:
        model = Comment
        fields = ("name", "email", "body")
