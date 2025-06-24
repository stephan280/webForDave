from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('paste/', views.paste_text, name='paste_text'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
