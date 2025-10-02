# quizzes/frontend_urls.py
from django.urls import path
from .frontend_views import index, quiz_page

urlpatterns = [
    path('', index, name='frontend-index'),
    path('quiz/<int:pk>/', quiz_page, name='frontend-quiz-detail'),
]
