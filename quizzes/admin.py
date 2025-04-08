import nested_admin
from django.contrib import admin
from .models import Quiz, Question, Answer

class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 2

class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInline]
    extra = 1

class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'type', 'module', 'chapter', 'created_by', 'creation_mode', 'created_at')

admin.site.register(Quiz, QuizAdmin)
