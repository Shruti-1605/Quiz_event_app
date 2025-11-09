from django.core.management.base import BaseCommand
from quiz_events_app.models import Quiz

class Command(BaseCommand):
    help = 'Update quiz categories based on title keywords'

    def handle(self, *args, **options):
        quizzes = Quiz.objects.all()
        updated = 0
        
        for quiz in quizzes:
            title_lower = quiz.title.lower()
            
            if 'python' in title_lower:
                quiz.category = 'python'
            elif 'java' in title_lower and 'javascript' not in title_lower:
                quiz.category = 'java'
            elif 'javascript' in title_lower or 'js' in title_lower:
                quiz.category = 'javascript'
            elif 'php' in title_lower:
                quiz.category = 'php'
            elif 'c++' in title_lower or 'cpp' in title_lower:
                quiz.category = 'cpp'
            elif 'c#' in title_lower or 'csharp' in title_lower:
                quiz.category = 'csharp'
            elif 'swift' in title_lower:
                quiz.category = 'swift'
            elif 'ruby' in title_lower:
                quiz.category = 'ruby'
            elif 'go' in title_lower and 'golang' in title_lower:
                quiz.category = 'go'
            elif 'rust' in title_lower:
                quiz.category = 'rust'
            elif 'kotlin' in title_lower:
                quiz.category = 'kotlin'
            else:
                quiz.category = 'general'
            
            quiz.save()
            updated += 1
            self.stdout.write(f'Updated: {quiz.title} -> {quiz.get_category_display()}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated} quizzes')
        )