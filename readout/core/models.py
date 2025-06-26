from django.db import models
from django.contrib.auth.models import User

class Conversion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    language = models.CharField(max_length=10, choices=[('english', 'English'), ('pidgin', 'Pidgin')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.language} - {self.created_at}"