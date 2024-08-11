from users.models import User
from catalog.forms import StyleFormMixin
from django.contrib.auth.forms import UserCreationForm


class UserRegForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
