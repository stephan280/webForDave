from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from gtts import gTTS
import uuid
import os
import fitz  # PyMuPDF
from django.conf import settings

def home(request):
    return render(request, 'main/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')

def process_text_to_speech(text_input):
    text_output = text_input.strip()
    audio_file_url = ""

    if text_output:
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        tts = gTTS(text_output)
        tts.save(filepath)
        audio_file_url = settings.MEDIA_URL + filename

    return text_output, audio_file_url

@login_required
def paste_text(request):
    text_output = audio_file_url = ""

    if request.method == 'POST':
        text_input = request.POST.get('pasted_text')
        text_output, audio_file_url = process_text_to_speech(text_input)

    return render(request, 'main/paste_text.html', {
        'text_output': text_output,
        'audio_file_url': audio_file_url
    })

@login_required
def upload_pdf(request):
    text_output = audio_file_url = ""

    if request.method == 'POST':
        uploaded_file = request.FILES.get('pdf_file')
        if uploaded_file and uploaded_file.name.endswith('.pdf'):
            pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = ""
            for page in pdf:
                text += page.get_text()
            pdf.close()
            text_output, audio_file_url = process_text_to_speech(text)

    return render(request, 'main/upload_pdf.html', {
        'text_output': text_output,
        'audio_file_url': audio_file_url
    })
