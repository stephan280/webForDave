from django import forms

class TextOrPDFForm(forms.Form):
    text_input = forms.CharField(
        label='Paste Text',
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Paste your content here...',
            'style': 'resize: vertical; max-height: 200px;'
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
