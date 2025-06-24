from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path("register/", views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path('upload/', views.upload, name='upload'),
    path('preview', views.preview, name='preview'),
    path('convert', views.convert_text_to_audio, name='convert'),
]
