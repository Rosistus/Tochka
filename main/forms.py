from django import forms
from main.models import BlessLimit
from django.core.validators import RegexValidator


class BlessLimitForm(forms.Form):
    limit = forms.CharField(validators=[RegexValidator(r'^\d{1,}$', message='Только цифрыы')],
                               required=False,
                               widget=forms.TextInput(attrs={'type': 'number',
                                                                            'class': 'input2',
                                                                            'placeholder': 'Изменить кол-во мест',
                                                                            }))

    class Meta:
        model = BlessLimit
        fields = ('limit',)
