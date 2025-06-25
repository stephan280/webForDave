from django.shortcuts import render, redirect
from .forms import ConversionForm
from django.shortcuts import get_object_or_404
import fitz
from .models import Conversion
from gtts import gTTS
import os
from django.core.files.base import ContentFile
from io import BytesIO

def upload_or_paste(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST, request.FILES)
        if form.is_valid():
            conversion = form.save(commit=False)

            if conversion.pdf_file:
                extracted_text = extract_text_from_pdf(conversion.pdf_file)
                conversion.pasted_text = extracted_text

            final_text = conversion.pasted_text

            # Check and convert text to audio
            if final_text:
                try:
                    print("🧠 Generating speech...")
                    tts = gTTS(text=final_text, lang='en')
                    mp3_fp = BytesIO()
                    tts.write_to_fp(mp3_fp)
                    mp3_fp.seek(0)
                    conversion.audio_file.save('audio.mp3', ContentFile(mp3_fp.read()), save=False)
                    print("✅ Audio saved successfully")
                except Exception as e:
                    print("❌ TTS conversion failed:", e)

            conversion.save()
            return redirect('conversion_detail', conversion_id=conversion.id)
    else:
        form = ConversionForm()
    return render(request, 'converter/upload.html', {'form': form})



def conversion_detail(request, conversion_id):
    conversion = get_object_or_404(Conversion, id=conversion_id)
    return render(request, 'converter/detail.html', {'conversion': conversion})

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text