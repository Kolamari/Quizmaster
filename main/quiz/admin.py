from django.contrib import admin
from .models import Course, Question, Option, QuizSettings, QuizAttempt, StudentAnswer


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4
    max_num = 4
    min_num = 4


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('code', 'name')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'text_preview', 'difficulty', 'is_active', 'created_at')
    list_filter = ('course', 'difficulty', 'is_active', 'created_at')
    search_fields = ('text',)
    inlines = [OptionInline]
    list_per_page = 20

    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Question Text'


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_preview', 'text_preview', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text', 'question__text')

    def question_preview(self, obj):
        return f"Q{obj.question.id}: {obj.question.text[:50]}..."
    question_preview.short_description = 'Question'

    def text_preview(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
    text_preview.short_description = 'Option Text'


@admin.register(QuizSettings)
class QuizSettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration_minutes', 'total_questions', 'passing_score', 'is_active', 'results_release_time')
    list_filter = ('is_active', 'shuffle_questions', 'shuffle_options')
    search_fields = ('title', 'course__name')
    fieldsets = (
        ('Basic Settings', {
            'fields': ('course', 'title', 'is_active')
        }),
        ('Quiz Configuration', {
            'fields': ('duration_minutes', 'total_questions', 'passing_score')
        }),
        ('Randomization', {
            'fields': ('shuffle_questions', 'shuffle_options')
        }),
        ('Results', {
            'fields': ('results_release_time', 'allow_multiple_attempts')
        }),
    )


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'score', 'total_questions', 'started_at', 'completed_at')
    list_filter = ('status', 'course')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('started_at', 'completed_at')


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct', 'answered_at')
    list_filter = ('is_correct',)
    search_fields = ('attempt__user__username', 'question__text')
