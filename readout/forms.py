from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class TextOrPDFForm(forms.Form):
    text_input = forms.CharField(
        label='Paste Text',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Paste your content here...',
            'style': 'resize: vertical; max-height: 200px;',
        }),
        required=False
    )

    pdf_file = forms.FileField(
        label='Upload PDF',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf'
        })
    )

    language = forms.ChoiceField(
        choices=[('en', 'English'), ('pidgin', 'Pidgin')],
        label='Choose Language',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text_input')
        file = cleaned_data.get('pdf_file')

        if not text and not file:
            raise forms.ValidationError("Please provide either text input or a PDF file.")
        return cleaned_data

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Enter {field.label.lower()}'
            })
