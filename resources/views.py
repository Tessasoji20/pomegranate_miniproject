from django.views import View
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app.models import Module
from resources.models import Resource
from django.http import JsonResponse
from resources.forms import ResourceForm


@method_decorator(login_required, name='dispatch')
class ResourceListView(View):

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)

        resource_type = request.GET.get('type')

        resources = Resource.objects.filter(module=module)

        if resource_type:
            resources = resources.filter(resource_type=resource_type)

        return render(request, 'dashboards/resources.html', {
            'module': module,
            'resources': resources,
            'selected_type': resource_type
        })
@method_decorator(login_required, name='dispatch')
class ResourceDetailView(View):

    def get(self, request, resource_id):
        resource = get_object_or_404(Resource, id=resource_id)

        return render(request, 'dashboards/resource_detail.html', {
            'resource': resource,
            'is_liked': resource.likes.filter(id=request.user.id).exists(),
            'is_saved': resource.saved_by.filter(id=request.user.id).exists(),
            'likes_count': resource.likes.count(),
            'comments': resource.comments.all()
        })



@method_decorator(login_required, name='dispatch')
class ToggleLikeView(View):
    def post(self, request, resource_id):
        resource = get_object_or_404(Resource, id=resource_id)
        user = request.user

        if resource.likes.filter(id=user.id).exists():
            resource.likes.remove(user)
            liked = False
        else:
            resource.likes.add(user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'likes_count': resource.likes.count()
        })

@method_decorator(login_required, name='dispatch')
class ToggleSaveView(View):
    def post(self, request, resource_id):
        resource = get_object_or_404(Resource, id=resource_id)
        user = request.user

        if resource.saved_by.filter(id=user.id).exists():
            resource.saved_by.remove(user)
            saved = False
        else:
            resource.saved_by.add(user)
            saved = True

        return JsonResponse({
            'saved': saved
        })


@method_decorator(login_required, name='dispatch')
class AddCommentView(View):
    def post(self, request, resource_id):
        text = request.POST.get('text')

        if not text:
            return JsonResponse({'error': 'Empty comment'}, status=400)

        resource = get_object_or_404(Resource, id=resource_id)

        comment = resource.comments.create(
            user=request.user,
            text=text
        )

        return JsonResponse({
            'username': comment.user.username,
            'text': comment.text,

        })
@method_decorator(login_required, name='dispatch')
class AddResourceView(View):
    def get(self, request, module_id):
        form = ResourceForm()
        module = get_object_or_404(Module, id=module_id)

        return render(request, 'dashboards/add_resource.html', {
            'form': form,
            'module': module
        })

    def post(self, request, module_id):
        form = ResourceForm(request.POST, request.FILES)
        module = get_object_or_404(Module, id=module_id)

        if form.is_valid():
            resource = form.save(commit=False)
            resource.module = module
            resource.uploaded_by = request.user
            resource.save()
            form.save_m2m()

            return redirect('resources:results', module_id=module.id)

        return render(request, 'dashboards/add_resource.html', {
            'form': form,
            'module': module
        })
