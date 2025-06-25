from django import forms
from .models import Conversion

class ConversionForm(forms.ModelForm):
    class Meta:
        model = Conversion
        fields = ['pdf_file', 'pasted_text']

    def clean(self):
        cleaned_data = super().clean()
        pdf = cleaned_data.get("pdf_file")
        text = cleaned_data.get("pasted_text")

        if not pdf and not text:
            raise forms.ValidationError("You must upload a PDF or paste some text.")
        return cleaned_data
