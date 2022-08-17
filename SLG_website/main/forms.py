from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, User
from captcha.fields import CaptchaField


class GeneratorForm(forms.Form):
    size_of_verse = forms.IntegerField(label='Размер куплета(кол-во пар строк):', initial=2, min_value=1, max_value=16)
    amount_verse = forms.IntegerField(label='Количество куплетов:', initial=2, min_value=1, max_value=16)
    amount_phrase_in_string = forms.IntegerField(
        label='Количество словосочетаний в строке куплета:',
        initial=2,
        min_value=2,
        max_value=4
    )
    size_of_chorus = forms.IntegerField(label='Размер припева(кол-во пар строк):', initial=2, min_value=1, max_value=8)
    amount_words_in_string = forms.IntegerField(
        label='Количество слов в строке припева:',
        initial=2,
        min_value=2,
        max_value=8
    )
    rhyme_type = forms.ChoiceField(
        label='Тип рифмы куплета:',
        choices=(('consistent', 'Последовательная'), ('cross', 'Перекрестная'))
    )


class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(label='Логин:')
    password1 = forms.CharField(label='Пароль:')
    password2 = forms.CharField(label='Подтверждение пароля:')
    captcha = CaptchaField(label='Введите код с картинки:')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин:')
    password = forms.CharField(label='Пароль:')
