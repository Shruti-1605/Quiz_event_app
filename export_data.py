import os
import django
import json
from django.core import serializers

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_events_project.settings')
django.setup()

from quiz_events_app.models import Quiz, Question, Answer, Event

def export_sample_data():
    """Export sample data without user information"""
    
    # Export Quizzes
    quizzes = Quiz.objects.all()
    quiz_data = serializers.serialize('json', quizzes)
    
    # Export Questions
    questions = Question.objects.all()
    question_data = serializers.serialize('json', questions)
    
    # Export Answers
    answers = Answer.objects.all()
    answer_data = serializers.serialize('json', answers)
    
    # Export Events
    events = Event.objects.all()
    event_data = serializers.serialize('json', events)
    
    # Save to files
    with open('sample_quizzes.json', 'w') as f:
        f.write(quiz_data)
    
    with open('sample_questions.json', 'w') as f:
        f.write(question_data)
    
    with open('sample_answers.json', 'w') as f:
        f.write(answer_data)
    
    with open('sample_events.json', 'w') as f:
        f.write(event_data)
    
    print("✅ Sample data exported successfully!")
    print("Files created: sample_quizzes.json, sample_questions.json, sample_answers.json, sample_events.json")

if __name__ == "__main__":
    export_sample_data()