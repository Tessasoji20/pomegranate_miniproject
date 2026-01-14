# app/context_processors.py
def user_academic_context(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, 'userprofile', None)
        return {
            'current_course': profile.course if profile else None,
            'current_semester': profile.semester if profile else None,
        }
    return {}
