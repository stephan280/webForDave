from django.shortcuts import render, redirect
from .forms import ConversionForm
from django.shortcuts import get_object_or_404
import fitz
from .models import Conversion
from gtts import gTTS
import os
from django.core.files.base import ContentFile
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def upload_or_paste(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST, request.FILES)
        if form.is_valid():
            conversion = form.save(commit=False)
            conversion.user = request.user 

            # STEP 1: Extract text
            if conversion.pdf_file:
                extracted_text = extract_text_from_pdf(conversion.pdf_file)
                conversion.pasted_text = extracted_text

            final_text = conversion.pasted_text

            # STEP 2: Convert to speech
            if final_text:
                try:
                    tts = gTTS(text=final_text, lang='en')
                    mp3_fp = BytesIO()
                    tts.write_to_fp(mp3_fp)
                    mp3_fp.seek(0)
                    conversion.audio_file.save('audio.mp3', ContentFile(mp3_fp.read()), save=False)
                except Exception as e:
                    print("TTS Error:", e)

            conversion.save()
            return redirect('conversion_detail', conversion_id=conversion.id)
    else:
        form = ConversionForm()
    return render(request, 'converter/upload.html', {'form': form})


@login_required
def conversion_detail(request, conversion_id):
    conversion = get_object_or_404(Conversion, id=conversion_id)
    return render(request, 'converter/detail.html', {'conversion': conversion})

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

@login_required
def dashboard(request):
    conversions = Conversion.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'converter/dashboard.html', {'conversions': conversions})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})