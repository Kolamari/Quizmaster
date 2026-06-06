import json
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib.auth.models import User
from .models import Course, Question, Option, QuizSettings, QuizAttempt, StudentAnswer


def get_or_create_default_course():
    """Get or create the default Software Engineering course."""
    course, created = Course.objects.get_or_create(
        code='SE101',
        defaults={
            'name': 'Software Engineering',
            'description': 'Introduction to Software Engineering principles and practices'
        }
    )
    return course


def get_or_create_quiz_settings(course):
    """Get or create quiz settings for a course."""
    settings, created = QuizSettings.objects.get_or_create(
        course=course,
        defaults={
            'title': f'{course.name} Quiz',
            'duration_minutes': 60,
            'total_questions': 50,
            'passing_score': 25,
            'shuffle_questions': True,
            'shuffle_options': True,
            'allow_multiple_attempts': False,
            'is_active': True
        }
    )
    return settings


@login_required
def quiz_dashboard(request):
    """Display quiz dashboard for students."""
    user = request.user
    
    # Check if user is lecturer
    if hasattr(user, 'profile') and user.profile.is_lecturer:
        return redirect('admin_dashboard')
    
    course = get_or_create_default_course()
    settings = get_or_create_quiz_settings(course)
    
    # Check for existing attempts
    attempts = user.quiz_attempts.filter(course=course).order_by('-started_at')
    current_attempt = attempts.filter(status='in_progress').first()
    completed_attempts = attempts.filter(status__in=['completed', 'timed_out'])
    
    can_take_quiz = True
    if not settings.allow_multiple_attempts and completed_attempts.exists():
        can_take_quiz = False
    
    results_released = settings.are_results_released()
    
    context = {
        'course': course,
        'settings': settings,
        'current_attempt': current_attempt,
        'completed_attempts': completed_attempts,
        'can_take_quiz': can_take_quiz,
        'results_released': results_released,
        'total_questions': Question.objects.filter(course=course, is_active=True).count(),
    }
    return render(request, 'quiz/dashboard.html', context)


@login_required
def start_quiz(request):
    """Start a new quiz attempt."""
    user = request.user
    
    if hasattr(user, 'profile') and user.profile.is_lecturer:
        messages.error(request, 'Lecturers cannot take quizzes.')
        return redirect('quiz_dashboard')
    
    course = get_or_create_default_course()
    settings = get_or_create_quiz_settings(course)
    
    # Check if quiz is active
    if not settings.is_active:
        messages.error(request, 'This quiz is currently not active.')
        return redirect('quiz_dashboard')
    
    # Check for existing in-progress attempt
    existing_attempt = user.quiz_attempts.filter(course=course, status='in_progress').first()
    if existing_attempt:
        messages.info(request, 'You have an ongoing quiz. Redirecting...')
        return redirect('take_quiz')
    
    # Check for completed attempts
    if not settings.allow_multiple_attempts:
        completed = user.quiz_attempts.filter(
            course=course,
            status__in=['completed', 'timed_out']
        ).first()
        if completed:
            messages.error(request, 'You have already completed this quiz. Multiple attempts are not allowed.')
            return redirect('quiz_dashboard')
    
    # Check if enough questions exist
    available_questions = Question.objects.filter(course=course, is_active=True)
    if available_questions.count() < settings.total_questions:
        messages.error(
            request, 
            f'Not enough questions available. Required: {settings.total_questions}, Available: {available_questions.count()}'
        )
        return redirect('quiz_dashboard')
    
    # Create new attempt
    with transaction.atomic():
        attempt = QuizAttempt.objects.create(
            user=user,
            course=course,
            total_questions=settings.total_questions,
            status='in_progress',
            time_remaining=settings.duration_minutes * 60
        )
        
        # Generate shuffled question order
        question_ids = list(available_questions.values_list('id', flat=True))
        random.shuffle(question_ids)
        attempt.question_order = question_ids[:settings.total_questions]
        attempt.save()
        
        # Pre-generate option shuffles
        option_mapping = {}
        for qid in attempt.question_order:
            question = Question.objects.get(id=qid)
            options = list(question.options.all())
            option_ids = [opt.id for opt in options]
            random.shuffle(option_ids)
            option_mapping[str(qid)] = option_ids
        attempt.option_mapping = option_mapping
        attempt.save()
    
    messages.success(request, 'Quiz started! Good luck!')
    return redirect('take_quiz')


@login_required
def take_quiz(request):
    """Display quiz questions for the student."""
    user = request.user
    
    # Get current attempt
    try:
        attempt = user.quiz_attempts.get(status='in_progress')
    except QuizAttempt.DoesNotExist:
        messages.error(request, 'No active quiz found. Please start a new quiz.')
        return redirect('quiz_dashboard')
    
    course = attempt.course
    settings = get_or_create_quiz_settings(course)
    
    # Calculate time remaining
    elapsed = (timezone.now() - attempt.started_at).total_seconds()
    total_time = settings.duration_minutes * 60
    remaining = max(0, total_time - elapsed)
    
    if remaining <= 0:
        # Time expired - auto submit
        grade_attempt(attempt)
        attempt.status = 'timed_out'
        attempt.completed_at = timezone.now()
        attempt.save()
        messages.warning(request, 'Time expired! Your quiz has been automatically submitted.')
        return redirect('quiz_results')
    
    # Get questions
    questions_data = []
    questions = attempt.get_shuffled_questions()
    
    # Get already answered questions
    answered = {
        ans.question_id: ans.selected_option_id 
        for ans in attempt.answers.all()
    }
    
    for idx, question in enumerate(questions, 1):
        options = attempt.get_shuffled_options(question)
        questions_data.append({
            'number': idx,
            'question': question,
            'options': options,
            'selected': answered.get(question.id)
        })
    
    context = {
        'attempt': attempt,
        'settings': settings,
        'questions_data': questions_data,
        'time_remaining': int(remaining),
        'total_time': total_time,
        'total_questions': len(questions_data),
    }
    return render(request, 'quiz/take_quiz.html', context)


@login_required
@require_POST
def save_answer(request):
    """Save a student's answer via AJAX."""
    try:
        attempt = request.user.quiz_attempts.get(status='in_progress')
    except QuizAttempt.DoesNotExist:
        return JsonResponse({'error': 'No active quiz'}, status=400)
    
    question_id = request.POST.get('question_id')
    option_id = request.POST.get('option_id')
    
    if not question_id or not option_id:
        return JsonResponse({'error': 'Missing data'}, status=400)
    
    try:
        question = Question.objects.get(id=question_id)
        selected_option = Option.objects.get(id=option_id, question=question)
    except (Question.DoesNotExist, Option.DoesNotExist):
        return JsonResponse({'error': 'Invalid question or option'}, status=400)
    
    # Update or create answer
    answer, created = StudentAnswer.objects.update_or_create(
        attempt=attempt,
        question=question,
        defaults={
            'selected_option': selected_option,
            'is_correct': selected_option.is_correct
        }
    )
    
    return JsonResponse({
        'success': True,
        'is_correct': selected_option.is_correct if attempt.status != 'in_progress' else None,
        'answered_count': attempt.answers.count()
    })


@login_required
def submit_quiz(request):
    """Submit the quiz and grade it."""
    user = request.user
    
    try:
        attempt = user.quiz_attempts.get(status='in_progress')
    except QuizAttempt.DoesNotExist:
        messages.error(request, 'No active quiz found.')
        return redirect('quiz_dashboard')
    
    # Grade the attempt
    grade_attempt(attempt)
    
    attempt.status = 'completed'
    attempt.completed_at = timezone.now()
    attempt.save()
    
    messages.success(request, f'Quiz submitted successfully! Your score will be available after results are released.')
    return redirect('quiz_results')


def grade_attempt(attempt):
    """Grade a quiz attempt."""
    correct_count = 0
    for answer in attempt.answers.all():
        if answer.is_correct:
            correct_count += 1
    
    attempt.score = correct_count
    attempt.save()


@login_required
def quiz_results(request):
    """Display quiz results."""
    user = request.user
    course = get_or_create_default_course()
    settings = get_or_create_quiz_settings(course)
    
    # Get latest completed attempt
    attempt = user.quiz_attempts.filter(
        course=course,
        status__in=['completed', 'timed_out']
    ).first()
    
    if not attempt:
        messages.info(request, 'You have not completed any quizzes yet.')
        return redirect('quiz_dashboard')
    
    # Check if results are released
    results_released = settings.are_results_released()
    
    context = {
        'attempt': attempt,
        'settings': settings,
        'results_released': results_released,
        'score_percentage': attempt.get_percentage(),
        'is_passed': attempt.is_passed(),
    }
    return render(request, 'quiz/results.html', context)


@login_required
def review_quiz(request):
    """Allow students to review their quiz with correct answers."""
    user = request.user
    course = get_or_create_default_course()
    settings = get_or_create_quiz_settings(course)
    
    # Check if results are released
    if not settings.are_results_released():
        messages.info(request, 'Results have not been released yet.')
        return redirect('quiz_results')
    
    # Get latest completed attempt
    attempt = user.quiz_attempts.filter(
        course=course,
        status__in=['completed', 'timed_out']
    ).first()
    
    if not attempt:
        messages.info(request, 'No completed quiz found.')
        return redirect('quiz_dashboard')
    
    # Build review data
    questions_data = []
    questions = attempt.get_shuffled_questions()
    
    # Get all answers for this attempt
    answers = {ans.question_id: ans for ans in attempt.answers.all()}
    
    for idx, question in enumerate(questions, 1):
        options = attempt.get_shuffled_options(question)
        answer = answers.get(question.id)
        
        questions_data.append({
            'number': idx,
            'question': question,
            'options': options,
            'selected_option': answer.selected_option if answer else None,
            'is_correct': answer.is_correct if answer else False,
            'correct_option': question.get_correct_option()
        })
    
    context = {
        'attempt': attempt,
        'settings': settings,
        'questions_data': questions_data,
        'score_percentage': attempt.get_percentage(),
        'is_passed': attempt.is_passed(),
    }
    return render(request, 'quiz/review.html', context)


# ==================== ADMIN VIEWS ====================

@staff_member_required
def admin_dashboard(request):
    """Admin dashboard for lecturers."""
    course = get_or_create_default_course()
    settings = get_or_create_quiz_settings(course)
    
    # Statistics
    total_questions = Question.objects.filter(course=course).count()
    active_questions = Question.objects.filter(course=course, is_active=True).count()
    total_students = User.objects.filter(
        profile__is_lecturer=False
    ).count()
    total_attempts = QuizAttempt.objects.filter(course=course).count()
    completed_attempts = QuizAttempt.objects.filter(
        course=course,
        status__in=['completed', 'timed_out']
    ).count()
    
    # Recent attempts
    recent_attempts = QuizAttempt.objects.filter(
        course=course
    ).select_related('user').order_by('-started_at')[:10]
    
    context = {
        'course': course,
        'settings': settings,
        'total_questions': total_questions,
        'active_questions': active_questions,
        'total_students': total_students,
        'total_attempts': total_attempts,
        'completed_attempts': completed_attempts,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'quiz/admin_dashboard.html', context)


@staff_member_required
def manage_questions(request):
    """Manage quiz questions."""
    course = get_or_create_default_course()
    questions = Question.objects.filter(course=course).prefetch_related('options')
    
    context = {
        'course': course,
        'questions': questions,
        'total_count': questions.count(),
    }
    return render(request, 'quiz/manage_questions.html', context)


@staff_member_required
def add_question(request):
    """Add a new question."""
    course = get_or_create_default_course()
    
    if request.method == 'POST':
        text = request.POST.get('text')
        difficulty = request.POST.get('difficulty', 'medium')
        explanation = request.POST.get('explanation', '')
        
        option_texts = request.POST.getlist('option_text[]')
        correct_option = request.POST.get('correct_option')
        
        if not text or len(option_texts) != 4 or correct_option is None:
            messages.error(request, 'Please fill in all fields and provide exactly 4 options.')
            return redirect('add_question')
        
        question = Question.objects.create(
            course=course,
            text=text,
            difficulty=difficulty,
            explanation=explanation
        )
        
        for i, opt_text in enumerate(option_texts):
            Option.objects.create(
                question=question,
                text=opt_text,
                is_correct=(str(i) == correct_option)
            )
        
        messages.success(request, 'Question added successfully!')
        return redirect('manage_questions')
    
    return render(request, 'quiz/add_question.html', {'course': course})


@staff_member_required
def edit_question(request, question_id):
    """Edit an existing question."""
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        question.text = request.POST.get('text')
        question.difficulty = request.POST.get('difficulty', 'medium')
        question.explanation = request.POST.get('explanation', '')
        question.save()
        
        option_texts = request.POST.getlist('option_text[]')
        correct_option = request.POST.get('correct_option')
        
        options = list(question.options.all())
        for i, opt in enumerate(options):
            if i < len(option_texts):
                opt.text = option_texts[i]
                opt.is_correct = (str(i) == correct_option)
                opt.save()
        
        messages.success(request, 'Question updated successfully!')
        return redirect('manage_questions')
    
    options = question.options.all()
    correct_index = None
    for i, opt in enumerate(options):
        if opt.is_correct:
            correct_index = i
            break
    
    context = {
        'question': question,
        'options': options,
        'correct_index': correct_index,
    }
    return render(request, 'quiz/edit_question.html', context)


@staff_member_required
def delete_question(request, question_id):
    """Delete a question."""
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    messages.success(request, 'Question deleted successfully!')
    return redirect('manage_questions')


@staff_member_required
def quiz_settings_view(request):
    """Manage quiz settings."""
    course = get_or_create_default_course()
    settings = get_or_create_quiz_settings(course)
    
    if request.method == 'POST':
        settings.title = request.POST.get('title', settings.title)
        settings.duration_minutes = int(request.POST.get('duration_minutes', 60))
        settings.total_questions = int(request.POST.get('total_questions', 50))
        settings.passing_score = int(request.POST.get('passing_score', 25))
        settings.shuffle_questions = request.POST.get('shuffle_questions') == 'on'
        settings.shuffle_options = request.POST.get('shuffle_options') == 'on'
        settings.allow_multiple_attempts = request.POST.get('allow_multiple_attempts') == 'on'
        settings.is_active = request.POST.get('is_active') == 'on'
        
        results_release = request.POST.get('results_release_time')
        if results_release:
            from datetime import datetime
            settings.results_release_time = datetime.fromisoformat(results_release)
        else:
            settings.results_release_time = None
        
        settings.save()
        messages.success(request, 'Quiz settings updated successfully!')
        return redirect('quiz_settings')
    
    context = {
        'course': course,
        'settings': settings,
    }
    return render(request, 'quiz/settings.html', context)


@staff_member_required
def view_results(request):
    """View all student results."""
    course = get_or_create_default_course()
    settings = get_or_create_quiz_settings(course)
    
    attempts = QuizAttempt.objects.filter(
        course=course,
        status__in=['completed', 'timed_out']
    ).select_related('user').order_by('-score', '-completed_at')
    
    # Statistics
    total_students = attempts.count()
    avg_score = 0
    pass_count = 0
    if total_students > 0:
        scores = [a.score or 0 for a in attempts]
        avg_score = sum(scores) / len(scores)
        pass_count = sum(1 for a in attempts if a.is_passed())
    
    context = {
        'course': course,
        'settings': settings,
        'attempts': attempts,
        'total_students': total_students,
        'avg_score': round(avg_score, 2),
        'pass_count': pass_count,
        'pass_rate': round((pass_count / total_students * 100), 2) if total_students > 0 else 0,
    }
    return render(request, 'quiz/view_results.html', context)


@staff_member_required
def import_questions(request):
    """Import questions from JSON or CSV."""
    import csv
    import json as json_mod
    
    course = get_or_create_default_course()
    
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            messages.error(request, 'Please select a file to upload.')
            return redirect('import_questions')
        
        file_name = file.name.lower()
        count = 0
        
        try:
            if file_name.endswith('.json'):
                data = json_mod.load(file)
                for item in data:
                    question = Question.objects.create(
                        course=course,
                        text=item.get('question', ''),
                        difficulty=item.get('difficulty', 'medium'),
                        explanation=item.get('explanation', '')
                    )
                    options = item.get('options', [])
                    correct = item.get('correct', 0)
                    for i, opt_text in enumerate(options):
                        Option.objects.create(
                            question=question,
                            text=opt_text,
                            is_correct=(i == correct)
                        )
                    count += 1
                    
            elif file_name.endswith('.csv'):
                decoded = file.read().decode('utf-8')
                reader = csv.DictReader(decoded.splitlines())
                for row in reader:
                    question = Question.objects.create(
                        course=course,
                        text=row.get('question', ''),
                        difficulty=row.get('difficulty', 'medium'),
                        explanation=row.get('explanation', '')
                    )
                    for i in range(4):
                        opt_key = f'option{i+1}'
                        Option.objects.create(
                            question=question,
                            text=row.get(opt_key, ''),
                            is_correct=(i == int(row.get('correct', 0)))
                        )
                    count += 1
            else:
                messages.error(request, 'Unsupported file format. Please upload JSON or CSV.')
                return redirect('import_questions')
            
            messages.success(request, f'{count} questions imported successfully!')
            return redirect('manage_questions')
            
        except Exception as e:
            messages.error(request, f'Error importing questions: {str(e)}')
            return redirect('import_questions')
    
    # Sample templates
    json_template = '[\n  {\n    "question": "What is Software Engineering?",\n    "difficulty": "easy",\n    "explanation": "Software Engineering is...",\n    "options": ["Option A", "Option B", "Option C", "Option D"],\n    "correct": 0\n  }\n]'
    csv_template = 'question,difficulty,explanation,option1,option2,option3,option4,correct\n"What is SE?","easy","SE is...","A","B","C","D",0'
    
    context = {
        'course': course,
        'json_template': json_template,
        'csv_template': csv_template,
    }
    return render(request, 'quiz/import_questions.html', context)
