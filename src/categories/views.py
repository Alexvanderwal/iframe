from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
# Create your views here.
from .models import Category


class CategoryListView(ListView):
    model = Category
    template_name = 'categories/category_list_view.html'

