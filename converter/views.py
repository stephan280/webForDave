from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import ConversionForm
from .models import Conversion
from gtts import gTTS
from django.core.files.base import ContentFile
from io import BytesIO
import fitz

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}, your account was created!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    conversions = Conversion.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'converter/dashboard.html', {'conversions': conversions})

@login_required
def upload_or_paste(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST, request.FILES)
        if form.is_valid():
            conversion = form.save(commit=False)
            conversion.user = request.user 

            if not conversion.pdf_file and not conversion.pasted_text:
                messages.error(request, "❌ Please upload a PDF or paste some text.")
                return render(request, 'converter/upload.html', {'form': form})

            if conversion.pdf_file:
                extracted_text = extract_text_from_pdf(conversion.pdf_file)
                conversion.pasted_text = extracted_text

            final_text = conversion.pasted_text

            if final_text and final_text.strip():
                try:
                    tts = gTTS(text=final_text, lang='en')
                    mp3_fp = BytesIO()
                    tts.write_to_fp(mp3_fp)
                    mp3_fp.seek(0)
                    conversion.audio_file.save('audio.mp3', ContentFile(mp3_fp.read()), save=False)
                except Exception as e:
                    messages.error(request, f"❌ TTS Error: {str(e)}")
                    return render(request, 'converter/upload.html', {'form': form})

            conversion.save()
            messages.success(request, "✅ Your file was converted successfully!")
            return redirect('conversion_detail', conversion_id=conversion.id)
    else:
        form = ConversionForm()

    return render(request, 'converter/upload.html', {'form': form})

@login_required
def conversion_detail(request, conversion_id):
    conversion = get_object_or_404(Conversion, id=conversion_id, user=request.user)
    return render(request, 'converter/detail.html', {'conversion': conversion})
