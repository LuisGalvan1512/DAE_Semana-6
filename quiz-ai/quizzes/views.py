from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Quiz, Question, Choice
from .serializers import (
    QuizSerializer, QuizDetailSerializer,
    QuestionSerializer, ChoiceSerializer,
    SubmitAnswerSerializer
)

# === Quiz ViewSet ===
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuizDetailSerializer
        return QuizSerializer

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        quiz = self.get_object()
        serializer = SubmitAnswerSerializer(data=request.data.get('answers', []), many=True)

        if not serializer.is_valid():
            return Response({
                'error': '❌ Invalid answer format',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        answers = serializer.validated_data
        results = []
        correct_count = 0

        for answer in answers:
            try:
                question = Question.objects.get(id=answer['question_id'], quiz=quiz)
                choice = Choice.objects.get(id=answer['choice_id'], question=question)

                is_correct = choice.is_correct
                if is_correct:
                    correct_count += 1

                results.append({
                    'question_id': question.id,
                    'question_text': question.text,
                    'choice_id': choice.id,
                    'choice_text': choice.text,
                    'is_correct': is_correct,
                    'emoji': '✅' if is_correct else '❌'
                })
            except (Question.DoesNotExist, Choice.DoesNotExist):
                results.append({
                    'question_id': answer['question_id'],
                    'error': '⚠️ Invalid question or choice'
                })

        total = len(results)
        percentage = round((correct_count / total) * 100, 2) if total > 0 else 0

        # Grading system
        if percentage >= 90:
            grade, emoji, message = 'A', '🏆', 'Outstanding!'
        elif percentage >= 80:
            grade, emoji, message = 'B', '🎉', 'Great job!'
        elif percentage >= 70:
            grade, emoji, message = 'C', '👍', 'Good work!'
        elif percentage >= 60:
            grade, emoji, message = 'D', '📚', 'Keep studying!'
        else:
            grade, emoji, message = 'F', '💪', 'Try again!'

        return Response({
            'quiz_id': quiz.id,
            'quiz_title': quiz.title,
            'total_questions': total,
            'correct_answers': correct_count,
            'incorrect_answers': total - correct_count,
            'score': f"{correct_count}/{total}",
            'percentage': percentage,
            'grade': grade,
            'emoji': emoji,
            'message': f"{emoji} {message} You got {correct_count} out of {total} correct!",
            'results': results
        })


# === Question & Choice ViewSets ===
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


# === API Root ===
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': '🧠 Welcome to Quiz.AI API',
        'version': 'v1.0',
        'description': 'Intelligent Quiz Management System',
        'features': [
            '✨ Create and manage quizzes',
            '❓ Add multiple-choice questions',
            '🎓 Submit answers and get instant grading',
            '📊 Track scores and performance'
        ],
        'workflow': [
            '1️⃣ Create a quiz (POST /quizzes/)',
            '2️⃣ Add questions (POST /questions/)',
            '3️⃣ Add choices (POST /choices/)',
            '4️⃣ View complete quiz (GET /quizzes/{id}/)',
            '5️⃣ Submit answers (POST /quizzes/{id}/submit/)'
        ],
        'endpoints': {
            'quizzes': reverse('quiz-list', request=request, format=format),
            'questions': reverse('question-list', request=request, format=format),
            'choices': reverse('choice-list', request=request, format=format),
        },
        'grading_system': {
            '90-100%': 'A 🏆 Outstanding',
            '80-89%': 'B 🎉 Great',
            '70-79%': 'C 👍 Good',
            '60-69%': 'D 📚 Pass',
            '0-59%': 'F 💪 Try Again'
        }
    })
