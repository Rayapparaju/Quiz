from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question
import random
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

@login_required(login_url='quiz:login')
def start_quiz(request):
    questions = list(Question.objects.all())
    random.shuffle(questions)

    question_ids = [q.id for q in questions]
    request.session['question_ids'] = question_ids
    request.session['score'] = 0
    request.session['question_number'] = 0
    return redirect('quiz:question')

def question_view(request):
    question_ids = request.session.get('question_ids', [])
    q_num = request.session.get('question_number', 0)

    if q_num >= len(question_ids):
        return redirect('quiz:result')

    question_id = question_ids[q_num]
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        selected = request.POST.get('choice')
        if selected:
            choice = question.choices.get(id=selected)
            if choice.is_correct:
                request.session['score'] += 1
        request.session['question_number'] += 1
        return redirect('quiz:question')

    return render(request, 'quiz/question.html', {'question': question})

def result_view(request):
    score = request.session.get('score', 0)
    total = Question.objects.count()
    return render(request, 'quiz/result.html', {'score': score, 'total': total})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz:start')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('quiz:start')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'quiz/login.html')

def logout_view(request):
    logout(request)
    return redirect('quiz:login')

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'quiz/login.html'

def quiz_home(request):
    return render(request, 'quiz/home.html')
