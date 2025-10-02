from rest_framework import serializers
from .models import Quiz, Question, Choice

# === Base Serializers ===
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text']


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


# === Enhanced Serializers ===
class ChoiceDetailSerializer(serializers.ModelSerializer):
    """For displaying choices without revealing correct answers"""
    class Meta:
        model = Choice
        fields = ['id', 'text']


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Question with all its choices"""
    choices = ChoiceDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']


class QuizDetailSerializer(serializers.ModelSerializer):
    """Complete quiz with questions and choices"""
    questions = QuestionDetailSerializer(many=True, read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'question_count', 'questions']

    def get_question_count(self, obj):
        return obj.questions.count()


# === For Answer Submission ===
class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    choice_id = serializers.IntegerField()
