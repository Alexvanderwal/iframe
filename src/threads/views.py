from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, ModelFormMixin
# Create your views here.
from django.db import transaction, IntegrityError

from .permissions import IsOwner
from .serializers import PostSerializer
from .models import Thread, Post
from .forms import PostForm, ThreadForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics
from django.contrib.auth.models import User


class ThreadListCreateView(ListView, ModelFormMixin):
    """
    Listview that loads a form to create a Thread.
    Shows either all Threads, or category specific threads.

    """
    model = Thread
    form_class = ThreadForm
    template_name = 'threads/thread_list_view.html'
    ordering = ['-date_updated']
    paginate_by = 40

    def get_success_url(self):
        try:
            return reverse('threads:detail-list', kwargs={'slug': self.kwargs.get('slug')})
        except:
            return reverse('threads:list')

    def get_queryset(self):
        if self.kwargs.get('slug'):
            self.queryset = Thread.objects.filter(category__slug=self.kwargs.get('slug')).order_by('-date_updated')
        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        self.object = None
        # Just here to prevent update bugs, referencing to a object this way is more robust.
        falseobj = Thread.objects.first()
        self.Category = falseobj.category.__class__

        initial_threadform_data = {'starter': self.request.user}
        if self.kwargs.get('slug'):
            initial_threadform_data['category'] = self.Category.objects.get(slug=self.kwargs.get('slug'))
        if self.request.user.is_authenticated:
            self.form = ThreadForm(
                initial=initial_threadform_data)
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
            pass
            # TODO: Render the forms again with validation errors

        # Whether the form validates or not, the view will be rendered by get()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        falseobj = Thread.objects.first()
        self.Category = falseobj.category.__class__
        # Just include the form
        context = super(ThreadListCreateView, self).get_context_data(*args, **kwargs)
        if self.kwargs.get('slug'):
            context['category'] = self.Category.objects.get(slug=self.kwargs.get('slug'))
        else:
            context['homepage'] = True
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


class UpdatePost(generics.RetrieveUpdateAPIView):
    """
    View one post, with the option to edit.

    * Requires the owner of the Post, or a Admin.
    * Requires token authentication.

    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,)


class DeletePost(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,)


class PostLikeAPIToggle(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, id=None):
        id = self.kwargs.get("id")
        obj = get_object_or_404(Post, id=id)
        url_ = obj.get_thread_url()
        user = self.request.user
        updated = False
        liked = False

        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True

        data = {
            "updated": updated,
            "liked": liked
        }

        return Response(data)