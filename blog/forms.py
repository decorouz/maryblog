from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=100)
    sender_email = forms.EmailField()
    receiver_email = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)
