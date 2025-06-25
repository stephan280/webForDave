from django.db import models
from django.contrib.auth.models import User

LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('pid', 'Pidgin'),
]

class Conversion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    pasted_text = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
