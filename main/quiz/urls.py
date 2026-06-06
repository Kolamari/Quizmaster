from django.urls import path
from . import views

urlpatterns = [
    # Student routes
    path('', views.quiz_dashboard, name='quiz_dashboard'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('take/', views.take_quiz, name='take_quiz'),
    path('save-answer/', views.save_answer, name='save_answer'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('results/', views.quiz_results, name='quiz_results'),
    path('review/', views.review_quiz, name='review_quiz'),
    
    # Admin routes
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/questions/', views.manage_questions, name='manage_questions'),
    path('admin/questions/add/', views.add_question, name='add_question'),
    path('admin/questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('admin/questions/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('admin/settings/', views.quiz_settings_view, name='quiz_settings'),
    path('admin/results/', views.view_results, name='view_results'),
    path('admin/import/', views.import_questions, name='import_questions'),
]
