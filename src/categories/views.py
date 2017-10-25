from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic import CreateView
# Create your views here.
from .models import Category

from .forms import CategoryForm


class CategoryListView(ListView):
    model = Category
    template_name = 'categories/category_list_view.html'


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'categories/category_create_view.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('categories:list')

