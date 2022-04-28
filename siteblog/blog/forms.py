from django import forms
from captcha.fields import CaptchaField


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ваше имя"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            'rows': 5,
            'cols': 10,
            "class": "form-control",
            "placeholder": "Оставьте комментарий"
        })
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "Введите существующий email"
        })
    )


class ContactForm(forms.Form):
    user_name = forms.CharField(label='Имя',
                                widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Ваше имя"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "Введите существующий email"
        }))
    content = forms.CharField(label='Текст', widget=forms.Textarea(
        attrs={'class': 'form-control', "rows": 5, "placeholder": "Сообщение..."}))
    captcha = CaptchaField()
