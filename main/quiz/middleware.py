import time
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import resolve
from django.contrib import messages
from .models import QuizAttempt


class QuizTimerMiddleware:
    """Middleware to handle quiz timer and auto-submission."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if user has an in-progress quiz attempt
        if request.user.is_authenticated:
            try:
                attempt = QuizAttempt.objects.get(
                    user=request.user,
                    status='in_progress'
                )
                
                # Calculate elapsed time
                elapsed = (timezone.now() - attempt.started_at).total_seconds()
                duration_seconds = attempt.course.settings.duration_minutes * 60
                remaining = max(0, duration_seconds - elapsed)
                
                # Store remaining time in request
                request.quiz_time_remaining = int(remaining)
                request.current_attempt = attempt
                
                # Check if time has expired
                if remaining <= 0 and attempt.status == 'in_progress':
                    self.auto_submit(request, attempt)
                    messages.warning(request, 'Your quiz time has expired. Your answers have been automatically submitted.')
                    return redirect('quiz_results')
                    
            except QuizAttempt.DoesNotExist:
                request.quiz_time_remaining = None
                request.current_attempt = None
        
        response = self.get_response(request)
        return response
    
    def auto_submit(self, request, attempt):
        """Automatically submit the quiz when time expires."""
        from .views import submit_quiz
        # Grade unansweredy questions as incorrect
        self._grade_attempt(attempt)
        attempt.status = 'timed_out'
        attempt.completed_at = timezone.now()
        attempt.save()
    
    def _grade_attempt(self, attempt):
        """Grade the quiz attempt."""
        correct_count = 0
        for answer in attempt.answers.all():
            if answer.is_correct:
                correct_count += 1
        
        # Count unanswered questions
        answered_questions = set(answer.question_id for answer in attempt.answers.all())
        all_questions = attempt.question_order
        unanswered = len(set(all_questions) - answered_questions)
        
        attempt.score = correct_count
        attempt.total_questions = len(all_questions)
        attempt.save()
