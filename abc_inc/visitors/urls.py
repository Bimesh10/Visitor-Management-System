from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('appointment_success/', views.appointment_success, name='appointment_success'),
    path('mark_completed/<int:visitor_id>/', views.mark_completed, name='mark_completed'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard URL
]
