from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
import fitz
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "main/home.html")

@login_required
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm
    return render(request, "main/signup.html", {"form": form})

def dashboard(request):
    text_output = ""

    if request.method == 'POST':
        # Check if user submitted pasted text
        if 'pasted_text' in request.POST:
            text_output = request.POST.get('pasted_text')

        # Check if user uploaded a PDF
        elif 'pdf_file' in request.FILES:
            uploaded_file = request.FILES['pdf_file']
            if uploaded_file.name.endswith('.pdf'):
                pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                for page in pdf:
                    text_output += page.get_text()
                pdf.close()
            else:
                text_output = "Only PDF files are supported."

    return render(request, 'main/dashboard.html', {'text_output': text_output})