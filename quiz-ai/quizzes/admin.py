# quizzes/admin.py
from django.contrib import admin
from .models import Quiz, Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'questions_count']
    search_fields = ['title', 'description']
    list_filter = ['created_at']
    inlines = [QuestionInline]

    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = 'Questions'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'quiz', 'choices_count']
    list_filter = ['quiz']
    search_fields = ['text']
    inlines = [ChoiceInline]

    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question'

    def choices_count(self, obj):
        return obj.choices.count()
    choices_count.short_description = 'Choices'

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'question_preview', 'is_correct']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['text']

    def question_preview(self, obj):
        return obj.question.text[:30] + "..." if len(obj.question.text) > 30 else obj.question.text
    question_preview.short_description = 'Question'
