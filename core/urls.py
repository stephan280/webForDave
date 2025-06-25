"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from converter import views as converter_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("converter.urls")),
    path('', include('django.contrib.auth.urls')),  # login, logout
    path('', converter_views.dashboard, name='dashboard'),  # default route
    path('upload/', converter_views.upload_or_paste, name='upload'),
    path('conversion/<int:conversion_id>/', converter_views.conversion_detail, name='conversion_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
