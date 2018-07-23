from django import forms

class PostForm(forms.Form):
    title = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea)

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

