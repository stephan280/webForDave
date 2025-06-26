from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ConversionForm
from .models import Conversion
try:
    from .utils import preprocess_pidgin
except ImportError:
    def preprocess_pidgin(text):
        messages.error(None, "Pidgin preprocessing unavailable. Using raw text.")
        return text
import PyPDF2
import threading
from gtts import gTTS
from django.core.files import File
import os
from django.conf import settings
from django.http import JsonResponse

def home(request):
    return render(request, 'core/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.error(request, 'Error creating account. Please check the form.')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def convert_text(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST, request.FILES)
        if form.is_valid():
            conversion = form.save(commit=False)
            conversion.user = request.user
            conversion.save()
            def process_conversion(conversion_obj):
                try:
                    if conversion_obj.pdf_file:
                        pdf_reader = PyPDF2.PdfReader(conversion_obj.pdf_file)
                        text = ''
                        for page in pdf_reader.pages:
                            extracted = page.extract_text()
                            if extracted:
                                text += extracted + ' '
                        conversion_obj.input_text = text.strip()
                    if not conversion_obj.input_text:
                        conversion_obj.input_text = "No text provided."
                    text_to_convert = preprocess_pidgin(conversion_obj.input_text) if conversion_obj.language == 'pidgin' else conversion_obj.input_text
                    tts = gTTS(text=text_to_convert, lang='en')
                    audio_path = os.path.join(settings.MEDIA_ROOT, 'audio', f'conversion_{conversion_obj.id}.mp3')
                    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
                    tts.save(audio_path)
                    with open(audio_path, 'rb') as f:
                        conversion_obj.audio_file.save(f'conversion_{conversion_obj.id}.mp3', File(f))
                    conversion_obj.save()
                except Exception as e:
                    print(f"Error processing conversion: {e}")
                    conversion_obj.input_text = f"Error: {str(e)}"
                    conversion_obj.save()
            threading.Thread(target=process_conversion, args=(conversion,)).start()
            return redirect('conversion_result', conversion_id=conversion.id)
        else:
            messages.error(request, 'Invalid input. Please check the form: ' + str(form.errors))
    else:
        form = ConversionForm()
    return render(request, 'core/convert_text.html', {'form': form})

@login_required
def conversion_result(request, conversion_id):
    try:
        conversion = Conversion.objects.get(id=conversion_id, user=request.user)
        return render(request, 'core/result.html', {'conversion': conversion})
    except Conversion.DoesNotExist:
        messages.error(request, 'Conversion not found or you do not have access.')
        return redirect('home')

@login_required
def check_audio_status(request, conversion_id):
    try:
        conversion = Conversion.objects.get(id=conversion_id, user=request.user)
        if conversion.input_text.startswith('Error:'):
            return JsonResponse({'audio_ready': False, 'error': conversion.input_text})
        if conversion.audio_file:
            return JsonResponse({'audio_ready': True, 'audio_url': conversion.audio_file.url})
        return JsonResponse({'audio_ready': False})
    except Conversion.DoesNotExist:
        return JsonResponse({'audio_ready': False, 'error': 'Conversion not found'}, status=404)