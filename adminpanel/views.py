from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from resources.models import Resource
from resources.models import Comment
from app.models import Module

User = get_user_model()


@method_decorator(login_required, name='dispatch')
class AdminDashboardView(View):
    def get(self, request):
        if not request.user.is_staff:
            return render(request, '403.html')

        return render(request, 'adminpanel/dashboard.html', {
            'post_count': Resource.objects.count(),
            'comment_count': Comment.objects.count(),
            'user_count': User.objects.count(),
        })


@method_decorator(login_required, name='dispatch')
class AdminPostListView(View):

    def get(self, request):
        # Permission check
        if not request.user.is_staff:
            return render(request, '403.html')

        # Get search query
        query = request.GET.get('q', '').strip()

        # Base queryset
        posts = Resource.objects.select_related(
            'uploaded_by', 'module'
        ).order_by('-created_at')

        # Apply search filter
        if query:
            posts = posts.filter(title__icontains=query)

        return render(request, 'adminpanel/posts.html', {
            'posts': posts,
            'query': query
        })

@method_decorator(login_required, name='dispatch')
class AdminPostDetailView(View):
    def get(self, request, post_id):
        if not request.user.is_staff:
            return render(request, '403.html')

        post = get_object_or_404(Resource, id=post_id)
        comments = post.comments.order_by('-created_at')

        return render(request, 'adminpanel/post_detail.html', {
            'post': post,
            'comments': comments
        })


@method_decorator(login_required, name='dispatch')
class AdminDeletePostView(View):
    def post(self, request, post_id):
        if not request.user.is_staff:
            return render(request, '403.html')

        Resource.objects.filter(id=post_id).delete()
        return redirect('admin_panel:posts')


@method_decorator(login_required, name='dispatch')
class AdminDeleteCommentView(View):
    def post(self, request, comment_id):
        if not request.user.is_staff:
            return render(request, '403.html')

        Comment.objects.filter(id=comment_id).delete()
        return redirect(request.META.get('HTTP_REFERER'))


@method_decorator(login_required, name='dispatch')
class AdminUsersView(View):
    def get(self, request):
        if not request.user.is_staff:
            return render(request, '403.html')

        # ✅ ONLY NON-ADMIN USERS
        users = User.objects.filter(is_staff=False).order_by('-date_joined')

        return render(request, 'adminpanel/users.html', {
            'users': users
        })


# @method_decorator(login_required, name='dispatch')
# class AdminSubjectsView(View):
#     def get(self, request):
#         if not request.user.is_staff:
#             return render(request, '403.html')
#
#         return render(request, 'adminpanel/subjects.html', {
#             'modules': Module.objects.all()
#
#         })
@method_decorator(login_required, name='dispatch')
class AdminFlaggedView(View):
    def get(self, request):
        if not request.user.is_staff:
            return render(request, '403.html')

        flagged_posts = Resource.objects.filter(is_flagged=True)
        flagged_comments = Comment.objects.filter(is_flagged=True)

        return render(request, 'adminpanel/flags.html', {
            'flagged_posts': flagged_posts,
            'flagged_comments': flagged_comments,
        })

@method_decorator(login_required, name='dispatch')
class AdminFlagPostView(View):
    def post(self, request, post_id):
        if not request.user.is_staff:
            return render(request, '403.html')

        Resource.objects.filter(id=post_id).update(is_flagged=True)
        return redirect('admin_panel:flags')

@method_decorator(login_required, name='dispatch')
class AdminFlagCommentView(View):
    def post(self, request, comment_id):
        if not request.user.is_staff:
            return render(request, '403.html')

        Comment.objects.filter(id=comment_id).update(is_flagged=True)
        return redirect('admin_panel:flags')
