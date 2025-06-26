from django import forms
from .models import Conversion
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class ConversionForm(forms.ModelForm):
    class Meta:
        model = Conversion
        fields = ['input_text', 'pdf_file', 'language']
        widgets = {
            'input_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Paste your text here...'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'language': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        input_text = cleaned_data.get('input_text')
        pdf_file = cleaned_data.get('pdf_file')
        if not input_text and not pdf_file:
            raise forms.ValidationError('Please provide either text or a PDF file.')
        return cleaned_data
    
class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Override widgets and suppress help_text
        for field_name, field in self.fields.items():
            field.help_text = ''  # ✂ Remove that default clutter
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label,
            })


class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Incorrect username or password. Try again.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label,
            })