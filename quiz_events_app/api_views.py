from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event
from .serializers import (
    QuizSerializer, QuizListSerializer, EventSerializer, 
    UserSubmissionSerializer, QuizSubmissionSerializer
)

class QuizListAPIView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer

class QuizDetailAPIView(generics.RetrieveAPIView):
    queryset = Quiz.objects.prefetch_related('questions__answers')
    serializer_class = QuizSerializer

class EventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    
    def get_queryset(self):
        return Event.objects.filter(date__gte=timezone.now()).order_by('date')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz_api(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QuizSubmissionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    answers_data = serializer.validated_data['answers']
    questions = quiz.questions.prefetch_related('answers').all()
    total_questions = questions.count()
    correct_count = 0
    
    submission = UserSubmission.objects.create(
        quiz=quiz,
        user=request.user,
        score=0
    )
    
    for question in questions:
        answer_id = answers_data.get(str(question.id))
        chosen_answer = None
        is_correct = False
        
        if answer_id:
            try:
                chosen_answer = Answer.objects.get(id=answer_id, question=question)
                is_correct = chosen_answer.is_correct
                if is_correct:
                    correct_count += 1
            except Answer.DoesNotExist:
                pass
        
        UserAnswer.objects.create(
            submission=submission,
            question=question,
            answer=chosen_answer,
            is_correct=is_correct
        )
    
    score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    submission.score = int(score)
    submission.save()
    
    return Response({
        'submission_id': submission.id,
        'score': submission.score,
        'correct_answers': correct_count,
        'total_questions': total_questions
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_history_api(request):
    submissions = UserSubmission.objects.filter(user=request.user).select_related('quiz').order_by('-submitted_at')
    serializer = UserSubmissionSerializer(submissions, many=True)
    return Response(serializer.data)