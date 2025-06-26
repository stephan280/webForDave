from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('convert/', views.convert_text, name='convert_text'),
    path('result/<int:conversion_id>/', views.conversion_result, name='conversion_result'),
]