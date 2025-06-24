from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomRegisterForm
from .forms import CustomLoginForm
import PyPDF2
from .forms import TextOrPDFForm
from gtts import gTTS
import os
from django.conf import settings
import uuid
from datetime import datetime
import random

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'readout/home.html')

def register(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomRegisterForm()
    return render(request, "readout/register.html", {'form': form})

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'registration/login.html'

@login_required
def dashboard(request):
    # Greeting based on time of day
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return render(request, 'readout/dashboard.html', {
        'greeting': greeting,
    })

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
            lang = form.cleaned_data.get('language')

            if pdf:
                text = extract_text_from_pdf(pdf)

            request.session['tts_text'] = text
            request.session['tts_lang'] = lang 
            return redirect('preview')

    else:
        form = TextOrPDFForm()
    return render(request, 'readout/upload.html', {'form': form})

@login_required
def preview(request):
    text = request.session.get('tts_text', '')
    return render(request, 'readout/preview.html', {'text': text})

@login_required
def convert_text_to_audio(request):
    text = request.session.get('tts_text', '')
    lang = request.session.get('tts_lang', 'en')

    if not text:
        return redirect('upload')

    if lang == 'pidgin':
        text = translate_to_pidgin(text)

    filename = f"{uuid.uuid4()}.mp3"
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    tts = gTTS(text, lang='en')  # Pidgin still uses English voice
    tts.save(file_path)

    return render(request, 'readout/audio_result.html', {
        'audio_file': settings.MEDIA_URL + filename
    })


def translate_to_pidgin(text):
    replacements = {
        'hello': 'howfar',
        'how are you': 'how you dey',
        'my name is': 'na me be',
        'I am': 'I dey',
        'you are': 'you dey',
        'good morning': 'morning o',
        'good evening': 'evening o',
        'what is': 'wetin be',
        'why': 'why na',
        'money': 'ego',
        'food': 'chop',
    }

    for key, value in replacements.items():
        text = text.replace(key, value).replace(key.capitalize(), value.capitalize())
    return text
