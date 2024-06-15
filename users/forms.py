from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,
                                                             'class': 'input',
                                                             'placeholder': 'Логин',
                                                             }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                                                 'class': 'input',
                                                                 'placeholder': 'Пароль',
                                                                 }))

    class Meta:
        model = User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'auutofocus': True,
                                                                            'class': 'input',
                                                                            'placeholder': 'Логин',
                                                                            }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input',
                                                                  'placeholder': 'Пароль',
                                                                  }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input',
                                                                  'placeholder': 'Пароль еще раз',
                                                                  }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'Null': True,
                                                                            'blank': True,
                                                                            'placeholder': 'Почта',
                                                                            'class': 'input',
                                                                            }))
    blessed = False

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'email',
            'blessed',
        )
