from django.contrib import admin
from .models import Course, Semester, UserProfile
from .models import Subject, Module, UserSubject


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('course', 'number')
    list_filter = ('course',)
    ordering = ('course', 'number')


# @adminpanel.register(Subject)
# class SubjectAdmin(adminpanel.ModelAdmin):
#     list_display = ('code', 'name', 'course', 'semester')
#     list_filter = ('course', 'semester')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'semester')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'number')
    list_filter = ('subject',)
    ordering = ('subject', 'number')

@admin.register(UserSubject)
class UserSubjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject')
    list_filter = ('subject',)
    search_fields = ('user__username', 'subject__name')

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

def generate_modules(modeladmin, request, queryset):
    for subject in queryset:
        for i in range(1, 6):
            Module.objects.get_or_create(subject=subject, number=i)

generate_modules.short_description = "Generate modules 1–5"

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'course', 'semester')
    list_filter = ('course', 'semester')
    inlines = [ModuleInline]
    actions = [generate_modules]


