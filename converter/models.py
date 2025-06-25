from django.db import models

class Conversion(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    pasted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Conversion(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    pasted_text = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

