from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_home, name='quiz_home'),         # homepage of quiz app
    path('start/', views.start_quiz, name='start'),      # start quiz page
    path('question/', views.question_view, name='question'),
    path('result/', views.result_view, name='result'),

    # Auth URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
