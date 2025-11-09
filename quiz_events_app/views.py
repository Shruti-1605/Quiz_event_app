from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


def home(request):
    if not request.user.is_authenticated:
        return redirect('quiz_events_app:login')
    
    latest_quizzes = Quiz.objects.order_by('-created_at')[:6]
    return render(request, 'quiz_events_app/home.html', {
        'quizzes': latest_quizzes
    })


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_events_app/quiz_list.html', {'quizzes': quizzes})


@login_required
@require_http_methods(["GET", "POST"])
def quiz_attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('answers').all()

    if request.method == 'GET':
        return render(request, 'quiz_events_app/quiz_attempt.html', {
            'quiz': quiz,
            'questions': questions
        })

    # POST processing
    total_questions = questions.count()
    correct_count = 0

    submission = UserSubmission.objects.create(
        quiz=quiz,
        user=request.user,
        score=0
    )

    for q in questions:
        key = f'question_{q.id}'
        ans_id = request.POST.get(key)
        chosen = None
        is_correct = False

        if ans_id:
            try:
                chosen = Answer.objects.get(id=int(ans_id), question=q)
                is_correct = chosen.is_correct
                if is_correct:
                    correct_count += 1
            except (Answer.DoesNotExist, ValueError):
                chosen = None
        UserAnswer.objects.create(
            submission=submission,
            question=q,
            answer=chosen,
            is_correct=is_correct
        )

    score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    submission.score = int(score)
    submission.submitted_at = timezone.now()
    submission.save()

    return redirect('quiz_events_app:quiz_result', submission_id=submission.id)


@login_required
def result(request, submission_id):
    submission = get_object_or_404(UserSubmission, id=submission_id, user=request.user)
    user_answers = submission.user_answers.select_related('question', 'answer').all()

    # prepare correct answers for template to avoid template method calls
    processed_answers = []
    for ua in user_answers:
        correct_answer = ua.question.answers.filter(is_correct=True).first()
        processed_answers.append({
            'ua': ua,
            'correct_answer': correct_answer
        })

    return render(request, 'quiz_events_app/result.html', {
        'submission': submission,
        'processed_answers': processed_answers
    })


@login_required
def events_list(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'quiz_events_app/events.html', {'events': events})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Registration successful! Please login.')
                return redirect('quiz_events_app:login')
    else:
        form = RegisterForm()
    return render(request, 'quiz_events_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('quiz_events_app:home')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'quiz_events_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('quiz_events_app:home')

@login_required
def quiz_history(request):
    submissions = UserSubmission.objects.filter(user=request.user).select_related('quiz').order_by('-submitted_at')
    
    # Calculate statistics
    total_attempts = submissions.count()
    passed_quizzes = submissions.filter(score__gte=60).count()
    average_score = 0
    if total_attempts > 0:
        total_score = sum(s.score for s in submissions)
        average_score = round(total_score / total_attempts)
    
    return render(request, 'quiz_events_app/quiz_history.html', {
        'submissions': submissions,
        'total_attempts': total_attempts,
        'passed_quizzes': passed_quizzes,
        'average_score': average_score
    })

@login_required
def user_quiz_attempts(request):
    # Show available quizzes for the user to attempt
    quizzes = Quiz.objects.all()
    # Get user's previous attempts for each quiz
    quiz_data = []
    for quiz in quizzes:
        attempts = UserSubmission.objects.filter(user=request.user, quiz=quiz).order_by('-submitted_at')[:3]
        quiz_data.append({
            'quiz': quiz,
            'attempts': attempts
        })
    
    return render(request, 'quiz_events_app/user_quiz_attempts.html', {
        'quiz_data': quiz_data
    })






