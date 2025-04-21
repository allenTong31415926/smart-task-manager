from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm
from tasks.models import Task, Project
from datetime import datetime, timedelta

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
        
    return render(request, 'web/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'web/dashboard.html', {
        'tasks': tasks,
        'projects': projects,
    })

@login_required
def analytics_view(request):
    today = datetime.now().date()
    start_week = today - timedelta(days=today.weekday())
    week_tasks = Task.objects.filter(
        assigned_to=request.user,
        status='done',
        created_at__date__range=(start_week, today)
    )

    weekday_summary = {day: 0 for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
    for task in week_tasks:
        weekday_summary[task.created_at.strftime('%A')] += 1

    return render(request, 'web/analytics.html', {
        'weekly_summary': weekday_summary
    })
