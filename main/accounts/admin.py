from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('student_id', 'department', 'is_lecturer')


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_is_lecturer')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__is_lecturer')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'profile__student_id')

    def get_is_lecturer(self, obj):
        return obj.profile.is_lecturer if hasattr(obj, 'profile') else False
    get_is_lecturer.short_description = 'Lecturer'
    get_is_lecturer.boolean = True


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'department', 'is_lecturer', 'created_at')
    list_filter = ('is_lecturer', 'department')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id')
