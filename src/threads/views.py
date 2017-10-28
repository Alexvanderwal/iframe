from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, ModelFormMixin
# Create your views here.
from django.db import transaction, IntegrityError
from .models import Thread, Post
from .forms import PostForm, ThreadForm


class ThreadListView(ListView, ModelFormMixin):
    model = Thread
    form_class = ThreadForm
    template_name = 'threads/thread_list_view.html'
    ordering = ['-date_updated']

    def get_success_url(self):
        try:
            return reverse('threads:detail-list', kwargs={'slug': self.kwargs.get('slug')})
        except:
            return reverse('threads:list')

    def get_queryset(self):
        """
        using this to handle different URL paramters.
        :return:
        """
        if self.kwargs.get('slug'):
            # TODO: Verander dit naar een query manager ofzo
            return Thread.objects.filter(category__slug=self.kwargs.get('slug')).order_by('-date_updated')
        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        self.object = None
        if self.request.user.is_authenticated:
            self.form = ThreadForm(initial={'starter': self.request.user})
            self.initial_post_form = PostForm(
                initial={'user': self.request.user})

        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # When the form is submitted, it will enter here
        self.thread_form = self.get_form(self.form_class)
        self.post_form = self.get_form(PostForm)

        if all((self.thread_form.is_valid(), self.post_form.is_valid())):
            initial_post = self.post_form.save()
            thread = self.thread_form.save(commit=False)
            thread.initial_post = initial_post
            thread.save()
            self.get_success_url()
        else:
            print('invalid')
            print(self.thread_form.errors)
            print(self.post_form.errors)
            # TODO: Render the forms again with validation errors

            # return self.render_to_response(self.get_context_data(form=self.form))

        # Whether the form validates or not, the view will be rendered by get()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        # Just include the form
        context = super(ThreadListView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            context['form'] = self.form
            context['initial_post_form'] = self.initial_post_form
            context['forms'] = [self.form, self.initial_post_form]
        return context


class ThreadDetailView(FormMixin, DetailView):
    model = Thread
    form_class = PostForm
    template_name = 'threads/thread_detail_view.html'

    def get_success_url(self):
        return reverse('threads:detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['form'] = PostForm(initial={'user': self.request.user, 'thread': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(ThreadDetailView, self).form_valid(form)
