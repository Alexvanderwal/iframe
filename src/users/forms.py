from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.template import Template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from .models import Profile
from string import Template

User = get_user_model()

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html = Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))


class SignUpForm(UserCreationForm):
    avatar = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = User
        fields = ['avatar', 'description', 'username', 'first_name', 'last_name', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        avatar = forms.ImageField(widget=PictureWidget)
        model = Profile
        fields = ['avatar', 'description']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
