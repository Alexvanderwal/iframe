from django import forms
from django.urls import reverse

from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description',  'active']


