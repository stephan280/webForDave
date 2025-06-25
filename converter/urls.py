from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_or_paste, name='upload'),
    path('conversion/<int:conversion_id>/', views.conversion_detail, name='conversion_detail'),
]
