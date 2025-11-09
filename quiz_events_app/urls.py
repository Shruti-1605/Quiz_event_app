from django.urls import path
from . import views

app_name = 'quiz_events_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/start/', views.quiz_attempt, name='quiz_attempt'),
    path('quizzes/result/<int:submission_id>/', views.result, name='quiz_result'),
    path('events/', views.events_list, name='events_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.quiz_history, name='quiz_history'),
    path('my-attempts/', views.user_quiz_attempts, name='user_quiz_attempts'),
]
