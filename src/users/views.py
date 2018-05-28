from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model, authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import redis
from .models import Profile
from .forms import SignUpForm, ProfileForm, UserForm

# Create your views here.

# Using this to reference the user prevents everything breaking if we implement a custom User Model.
User = get_user_model()


class UserCreateView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/user_registration.html'
    success_url = '/'


    def get_context_data(self, *args, **kwargs):

        context['categories'] = self.Category.objects.all()
        
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
    model = Profile
    template_name = 'users/user_detail_view.html'
    context_object_name = 'object'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Profile,
            slug=self.kwargs['slug'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


@method_decorator(login_required, name='dispatch')
class UserAndProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/edit-view.html'


    def get_context_data(self, **kwargs):
        if self.object.user != self.request.user:
            raise Http404
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(self.request.POST or None, instance=self.object.user)
        context['profile_form'] = ProfileForm(self.request.POST, instance=self.object)
        context['forms'] = [context.get('user_form'), context.get('profile_form')]
        print('lol')
        return context

    def form_valid(self, form):
        context = self.get_context_data()

        form1 = context['user_form']
        form2 = context['profile_form']
        print(form1.is_valid())
        print(form2.is_valid())
        print(form2.errors)

        if all((form1.is_valid(), form2.is_valid())):
            user = form1.save()
            print(user)
            profile = form2.save(commit=False)
            profile.user = user
            profile.save()
            # TODO: Must b fixed
            return redirect('users:profile',slug=profile.slug)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form, *args, **kwargs):
        response = super().form_invalid(form, *args, **kwargs)
        print(form)
        return response


@login_required
def update_password(request, slug=None):
    user = User.objects.get(profile__slug=slug)
    if user != request.user:
        raise Http404

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            # messages.success(request, 'Your password was successfully updated!')
            return redirect('users:update_password')
        else:
            pass
            # messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/update-password.html', {
        'form': form
    })


# class UpdatePassword(UpdateView):
#     form_class = PasswordChangeForm
#     model = User
#     template_name =
#     success_url = '/'
#     slug_field = 'profile__slug'
#
#
#     def form_valid(self, form):
#         user = form.save()
#         update_session_auth_hash(self.request, user)
#         return super().form_valid(form)

# class UserEditView(UpdateView):
#     model = Profile
#     form_class = UserEditForm
#     context_object_name = 'object'
#     template_name = 'users/edit-view.html'