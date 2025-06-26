from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ConversionForm
from .models import Conversion
import PyPDF2
import threading

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
            if conversion.pdf_file:
                # Extract text from PDF in a separate thread
                def extract_pdf_text(conversion_obj):
                    pdf_reader = PyPDF2.PdfReader(conversion_obj.pdf_file)
                    text = ''
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ''
                    conversion_obj.input_text = text
                    conversion_obj.save()
                
                threading.Thread(target=extract_pdf_text, args=(conversion,)).start()
            else:
                conversion.save()
            return redirect('conversion_result', conversion_id=conversion.id)
    else:
        form = ConversionForm()
    return render(request, 'core/convert_text.html', {'form': form})

@login_required
def conversion_result(request, conversion_id):
    conversion = Conversion.objects.get(id=conversion_id, user=request.user)
    return render(request, 'core/result.html', {'conversion': conversion})