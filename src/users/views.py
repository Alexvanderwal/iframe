from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model, authenticate, login

from .forms import SignUpForm
# Create your views here.

# Using this to reference the user prevents everything breaking if we implement a custom User Model.
User = get_user_model()


class UserCreateView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/user_registration.html'
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save()
        user.refresh_from_db()
        print(form.cleaned_data.get('avatar'))
        user.profile.avatar = form.cleaned_data.get('avatar')
        user.profile.description = form.cleaned_data.get('description')
        user.profile.save()
        user.save()
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail_view.html'
    context_object_name = 'object'
