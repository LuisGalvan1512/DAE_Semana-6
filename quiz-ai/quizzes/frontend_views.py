# quizzes/frontend_views.py
from django.shortcuts import render

def index(request):
    # la plantilla va a solicitar la lista vía JS al endpoint /api/v1/quizzes/
    return render(request, 'quizzes/index.html')

def quiz_page(request, pk):
    # pasamos solo el id; el JS cargará el detalle desde /api/v1/quizzes/{id}/
    return render(request, 'quizzes/quiz_detail.html', {'quiz_id': pk})
