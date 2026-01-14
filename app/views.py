from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from app.forms import UserRegistrationForm,LoginForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app.models import Semester,Course,UserProfile
from app.models import Subject,Module,UserSubject
from resources.models import Resource

# Create your views here.
class SplashView(View):
    def get(self,request):
        return render(request,'splash.html')

from app.models import UserProfile

class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # ✅ ADMIN REDIRECT (FIRST PRIORITY)
            if user.is_staff:
                return redirect('admin_panel:dashboard')

            # ✅ SAFE PROFILE ACCESS FOR NORMAL USERS
            profile, _ = UserProfile.objects.get_or_create(user=user)

            if profile.course is None:
                return redirect('app:choose_course')

            if profile.semester is None:
                return redirect('app:choose_semester')

            return redirect('app:dashboard')

        return render(request, 'login.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('app:userlogin')

class Register(View):

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('app:userlogin')

        # IMPORTANT: return the same form with errors
        return render(request, 'register.html', {'form': form})


class HomeView(View):
    def get(self, request):
        saved_posts = (
            request.user.saved_resources
            .select_related('module')
            .order_by('-id')
        )
        return render(request, 'dashboards/dashboard.html', {
            'saved_posts': saved_posts
        })

@method_decorator(login_required, name='dispatch')
class ChooseCourseView(View):

    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'choose_course.html', {'courses': courses})

    def post(self, request):
        profile = request.user.userprofile
        course_id = request.POST.get('course')

        if course_id:
            profile.course_id = course_id
            profile.semester = None  # reset semester if course changes
            profile.save()
            return redirect('app:choose_semester')

        courses = Course.objects.all()
        return render(request, 'choose_course.html', {'courses': courses})

@method_decorator(login_required, name='dispatch')
class ChooseSemesterView(View):

    def get(self, request):
        profile = request.user.userprofile

        # 🚫 Course must be selected first
        if not profile.course:
            return redirect('choose_course')

        semesters = Semester.objects.filter(course=profile.course)
        return render(request, 'choose_semester.html', {'semesters': semesters})

    def post(self, request):
        profile = request.user.userprofile

        if not profile.course:
            return redirect('choose_course')

        sem_id = request.POST.get('semester')

        if sem_id:
            profile.semester_id = sem_id
            profile.save()
            return redirect('app:dashboard')

        semesters = Semester.objects.filter(course=profile.course)
        return render(request, 'choose_semester.html', {'semesters': semesters})

class SelectSubjects(View):
    def get(self, request):
        return render(request, 'select_subjects.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):

    def get(self, request):
        profile = request.user.userprofile
        uploaded_posts = Resource.objects.filter(
            uploaded_by=request.user
        ).order_by('-created_at')

        context = {
            'user': request.user,
            'profile': profile,
            'uploaded_posts': uploaded_posts,
        }
        return render(request, 'dashboards/profile.html', context)

@method_decorator(login_required, name='dispatch')
class ChooseSubjectView(View):

    def get(self, request):
        profile = request.user.userprofile

        # Safety check
        if not profile.course or not profile.semester:
            return redirect('app:choose_course')

        subjects = Subject.objects.filter(
            course=profile.course,
            semester=profile.semester
        )

        return render(request, 'dashboards/select_subjects.html', {
            'subjects': subjects
        })

@method_decorator(login_required, name='dispatch')
class ChooseModuleView(View):

    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)

        modules = Module.objects.filter(subject=subject).order_by('number')

        return render(request, 'dashboards/choose_module.html', {
            'subject': subject,
            'modules': modules
        })