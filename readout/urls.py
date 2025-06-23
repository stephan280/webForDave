from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("register/", views.register, name='register'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path('upload/', views.upload, name='upload'),
    path('preview', views.preview, name='preview'),
    path('convert', views.convert_text_to_audio, name='convert'),
]
