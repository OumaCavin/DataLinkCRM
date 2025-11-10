"""
Projects views for DataLinkCRM.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Project

@login_required
def index(request):
    """Project list view."""
    projects = Project.objects.filter(user=request.user)
    context = {
        'title': 'Projects',
        'projects': projects,
    }
    return render(request, 'projects/index.html', context)

@login_required
def detail(request, project_id):
    """Project detail view."""
    project = get_object_or_404(Project, id=project_id, user=request.user)
    context = {
        'title': project.name,
        'project': project,
    }
    return render(request, 'projects/detail.html', context)

@login_required
def create(request):
    """Project create view."""
    context = {
        'title': 'Add Project',
    }
    return render(request, 'projects/form.html', context)
