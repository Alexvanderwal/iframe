from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import ModelFormMixin
from django.views.generic import CreateView
# Create your views here.
from .models import Category

from .forms import CategoryForm


class CategoryListView(ListView, ModelFormMixin):

    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_list_view.html'
    paginate_by = 40

    def get_success_url(self):
        return reverse('categories:list')

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = CategoryForm(None)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # When the form is submitted, it will enter here
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.form.save()
            self.get_success_url()
        else:
            # self.form.is_invalid()
            print('invalid')
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        # Just include the form
        context = super().get_context_data(*args, **kwargs)

        context['form'] = self.form
        return context


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'categories/category_create_view.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('categories:list')

