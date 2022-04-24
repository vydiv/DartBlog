from django import forms


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
