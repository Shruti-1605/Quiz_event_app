from django.contrib import admin
from .models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(UserSubmission)
admin.site.register(UserAnswer)
admin.site.register(Event)
