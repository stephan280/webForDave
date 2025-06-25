from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
    path('upload/', views.upload_or_paste, name='upload'),
    path('conversion/<int:conversion_id>/', views.conversion_detail, name='conversion_detail'),
    path('conversion/<int:conversion_id>/delete/', views.delete_conversion, name='delete_conversion'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('conversion/<int:conversion_id>/audio/', views.stream_audio, name='stream_audio'),
]
