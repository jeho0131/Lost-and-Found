from django import forms
from .models import LostItemPost, Comment

class LostItemPostForm(forms.ModelForm):
    class Meta:
        model = LostItemPost
        fields = ['title', 'description', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
