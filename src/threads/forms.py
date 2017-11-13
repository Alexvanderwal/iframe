from django import forms
from froala_editor.widgets import FroalaEditor

from .models import Post, Thread


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'thread']
        widgets = {
            'user': forms.HiddenInput(),
            'thread': forms.HiddenInput()
        }


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'category', 'starter']
        widgets = {
            'starter': forms.HiddenInput(),
            # 'category': forms.HiddenInput(),
        }


