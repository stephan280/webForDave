from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import PyPDF2
from .forms import TextOrPDFForm
from gtts import gTTS
import os
from django.conf import settings
import uuid  # for unique filename

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'readout/home.html')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "readout/register.html", {'form': form})

@login_required
def dashboard(request):
    return render(request, 'readout/dashboard.html')

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    return full_text

@login_required
def upload(request):
    if request.method == 'POST':
        form = TextOrPDFForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data.get('text_input')
            pdf = form.cleaned_data.get('pdf_file')

            if pdf:
                text = extract_text_from_pdf(pdf)

            # Store the extracted text in session (temp) for next step
            request.session['tts_text'] = text
            return redirect('preview')
    else:
        form = TextOrPDFForm()
    return render(request, 'readout/upload.html', {'form': form})

@login_required
def preview(request):
    text = request.session.get('tts_text', '')
    return render(request, 'readout/preview.html', {'text': text})

def convert_text_to_audio(request):
    text = request.session.get('tts_text', '')
    if not text:
        return redirect('upload') # this is return user if there is not text

    # Generate unique filename
    filename = f"{uuid.uuid4()}.mp3"
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Convert text to speech
    tts = gTTS(text)
    tts.save(file_path)

    # Pass path to template
    return render(request, 'readout/audio_result.html', {
        'audio_file': settings.MEDIA_URL + filename
    })