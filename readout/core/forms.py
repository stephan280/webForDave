from django import forms
from .models import Conversion

class ConversionForm(forms.ModelForm):
    class Meta:
        model = Conversion
        fields = ['input_text', 'pdf_file', 'language']
        widgets = {
            'input_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Paste your text here...'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'language': forms.Select(attrs={'class': 'form-select'}),
        }