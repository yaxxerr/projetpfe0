from django.contrib import admin
from .models import Quiz, Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'module', 'chapter', 'created_by', 'creation_mode', 'created_at')
    list_filter = ('type', 'creation_mode', 'module')
    search_fields = ('title',)
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'text')
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')