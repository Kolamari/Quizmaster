import random
import json
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Course(models.Model):
    """Course model for organizing quizzes."""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Question(models.Model):
    """Question model for storing quiz questions."""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    explanation = models.TextField(blank=True, help_text="Explanation for the correct answer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Q{self.id}: {self.text[:80]}..."

    def get_correct_option(self):
        """Get the correct option for this question."""
        return self.options.filter(is_correct=True).first()


class Option(models.Model):
    """Option model for question choices."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.text[:60]}..."


class QuizSettings(models.Model):
    """Quiz settings model for configuration."""
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='settings')
    title = models.CharField(max_length=200, default="Software Engineering Quiz")
    duration_minutes = models.PositiveIntegerField(default=60, help_text="Quiz duration in minutes")
    total_questions = models.PositiveIntegerField(default=50)
    passing_score = models.PositiveIntegerField(default=25, help_text="Minimum score to pass")
    results_release_time = models.DateTimeField(null=True, blank=True, help_text="When to release results")
    shuffle_questions = models.BooleanField(default=True, help_text="Randomize question order")
    shuffle_options = models.BooleanField(default=True, help_text="Randomize option order")
    allow_multiple_attempts = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Quiz Settings'

    def __str__(self):
        return f"{self.title} - {self.duration_minutes} mins"

    def are_results_released(self):
        """Check if results should be released."""
        if self.results_release_time is None:
            return True
        return timezone.now() >= self.results_release_time


class QuizAttempt(models.Model):
    """Model to track quiz attempts by students."""
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('timed_out', 'Timed Out'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    total_questions = models.PositiveIntegerField(default=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    question_order = models.JSONField(default=list, help_text="Shuffled question IDs")
    option_mapping = models.JSONField(default=dict, help_text="Shuffled option mappings per question")
    time_remaining = models.PositiveIntegerField(null=True, blank=True, help_text="Time remaining in seconds")

    class Meta:
        ordering = ['-started_at']
        unique_together = ['user', 'course', 'status']

    def __str__(self):
        return f"{self.user.username} - {self.course.code} - {self.status}"

    def get_shuffled_questions(self):
        """Get questions in shuffled order."""
        if not self.question_order:
            questions = list(Question.objects.filter(course=self.course, is_active=True))
            random.shuffle(questions)
            self.question_order = [q.id for q in questions]
            self.save(update_fields=['question_order'])
        else:
            questions = list(Question.objects.filter(id__in=self.question_order, is_active=True))
            questions.sort(key=lambda q: self.question_order.index(q.id))
        return questions

    def get_shuffled_options(self, question):
        """Get options in shuffled order for a question."""
        qid = str(question.id)
        options = list(question.options.all())
        
        if not self.option_mapping or qid not in self.option_mapping:
            original_ids = [opt.id for opt in options]
            shuffled_ids = original_ids.copy()
            random.shuffle(shuffled_ids)
            if not self.option_mapping:
                self.option_mapping = {}
            self.option_mapping[qid] = shuffled_ids
            self.save(update_fields=['option_mapping'])
        else:
            shuffled_ids = self.option_mapping[qid]
            options_dict = {opt.id: opt for opt in options}
            options = [options_dict[oid] for oid in shuffled_ids if oid in options_dict]
        
        return options

    def get_percentage(self):
        """Calculate percentage score."""
        if self.score is None or self.total_questions == 0:
            return 0
        return round((self.score / self.total_questions) * 100, 2)

    def is_passed(self):
        """Check if the student passed."""
        try:
            settings = self.course.settings
            return self.score is not None and self.score >= settings.passing_score
        except QuizSettings.DoesNotExist:
            return self.score is not None and self.score >= 25


class StudentAnswer(models.Model):
    """Model to store student answers."""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['attempt', 'question']

    def __str__(self):
        return f"{self.attempt.user.username} - Q{self.question.id}: {'Correct' if self.is_correct else 'Incorrect'}"
