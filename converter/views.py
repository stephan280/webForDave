from django.shortcuts import render, redirect
from .forms import ConversionForm
from django.shortcuts import get_object_or_404
import fitz
from .models import Conversion

def upload_or_paste(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST, request.FILES)
        if form.is_valid():
            conversion = form.save()
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

def upload_or_paste(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST, request.FILES)
        if form.is_valid():
            conversion = form.save(commit=False)

            if conversion.pdf_file:
                extracted_text = extract_text_from_pdf(conversion.pdf_file)
                conversion.pasted_text = extracted_text  # override any empty field
            # else: use the pasted_text already submitted

            conversion.save()
            return redirect('conversion_detail', conversion_id=conversion.id)
    else:
        form = ConversionForm()
    return render(request, 'converter/upload.html', {'form': form})