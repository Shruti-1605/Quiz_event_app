from django.urls import path
from .api_views import (
    QuizListAPIView, QuizDetailAPIView, EventListAPIView,
    submit_quiz_api, quiz_history_api
)

app_name = 'quiz_api'

urlpatterns = [
    path('quizzes/', QuizListAPIView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
    path('quizzes/<int:quiz_id>/submit/', submit_quiz_api, name='quiz-submit'),
    path('events/', EventListAPIView.as_view(), name='event-list'),
    path('history/', quiz_history_api, name='quiz-history'),
]