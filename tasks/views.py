from django.shortcuts import render, get_object_or_404, redirect
from .forms import FeedbackForm, ProjectForm, TaskForm
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from quality_control import views
from .models import Project, Task
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.template.loader import render_to_string
from django.views.generic.edit import UpdateView, DeleteView


#FBV version 1

"""def index(request):
    another_page_url = reverse('tasks:another_page')
    quality_control_url = 'quality_control/'
    html = f"<h1>Страница приложения tasks</h1><a href='{another_page_url}'>Перейти на другую страницу</a><br/><a href='{quality_control_url}'>Страница системы контроля качества</a>"
    return HttpResponse(html)

def index(request):
    projects_list_url = reverse('tasks:projects_list')
    html = f"<h1>Страница приложения tasks</h1><a href='{projects_list_url}'>Список проектов</a>"
    return HttpResponse(html)
    
def another_page(request):
    return HttpResponse("Это другая страница приложения tasks.")

def projects_list(request):
    projects = Project.objects.all()
    projects_html = '<h1>Список проектов</h1><ul>'
    for project in projects:
        projects_html += f'<li><a href="{project.id}/">{project.name}</a></li>'
    projects_html += '</ul>'
    return HttpResponse(projects_html)   

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    response_html = f'<h1>{project.name}</h1><p>{project.description}</p>'
    response_html += '<h2>Задачи</h2><ul>'
    for task in tasks:
        response_html += f'<li><a href="tasks/{task.id}/">{task.name}</a></li>'
    response_html += '</ul>'
    return HttpResponse(response_html) 

def task_detail(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)
    response_html = f'<h1>{task.name}</h1><p>{task.description}</p>'
    return HttpResponse(response_html)
    """

#CBV version 1

"""class IndexView(View):
    def get(self, request, *args, **kwargs):
        projects_list_url = reverse('tasks:projects_list')
        html = f"<h1>Страница приложения tasks</h1><a href='{projects_list_url}'>Список проектов</a>"
        return HttpResponse(html)
        
class ProjectsListView(ListView):
    model = Project

    def get(self, request, *args, **kwargs):
        projects = self.get_queryset()
        projects_html = '<h1>Список проектов</h1><ul>'
        for project in projects:
            projects_html += f'<li><a href="{project.id}/">{project.name}</a></li>'
        projects_html += '</ul>'
        return HttpResponse(projects_html)

class ProjectDetailView(DetailView):
    model = Project
    pk_url_kwarg = 'project_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        project = self.object
        tasks = project.tasks.all()
        response_html = f'<h1>{project.name}</h1><p>{project.description}</p>'
        response_html += '<h2>Задачи</h2><ul>'
        for task in tasks:
            response_html += f'<li><a href="tasks/{task.id}/">{task.name}</a></li>'
        response_html += '</ul>'
        return HttpResponse(response_html)

class TaskDetailView(DetailView):
    model = Task
    pk_url_kwarg = 'task_id'

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        response_html = f'<h1>{task.name}</h1><p>{task.description}</p>'
        return HttpResponse(response_html)
"""

#FBV version 2 - шаблоны

"""def index(request):
    return render(request, 'tasks/index.html')

def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'tasks/projects_list.html', {'project_list': projects})

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'tasks/project_detail.html', {'project': project})

def task_detail(request, project_id, task_id):
    task = get_object_or_404(Task, id=task_id, project_id=project_id)
    return render(request, 'tasks/task_detail.html', {'task': task})
"""

#CBV version 2 - шаблоны

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tasks/index.html')

class ProjectsListView(ListView):
    model = Project
    template_name = 'tasks/projects_list.html'

class ProjectDetailView(DetailView):
    model = Project
    pk_url_kwarg = 'project_id'
    template_name = 'tasks/project_detail.html'
    
class TaskDetailView(DetailView):
    model = Task
    pk_url_kwarg = 'task_id'
    template_name = 'tasks/task_detail.html'

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            return redirect('/tasks')
    else:
        form = FeedbackForm()
    return render(request, 'tasks/feedback.html', {'form': form})

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:projects_list')
    else:
        form = ProjectForm()
    return render(request, 'tasks/project_create.html', {'form': form})

def add_task_to_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('tasks:project_detail', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form, 'project': project})

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/project_create.html'
    success_url = reverse_lazy('tasks:projects_list')

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tasks:project_detail', kwargs={'project_id': self.kwargs['project_id']})

#FBV Update
"""
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('tasks:project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'tasks/project_update.html', {'form': form, 'project': project})

def update_task(request, project_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_detail', project_id=project_id, task_id=task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_update.html', {'form': form, 'task': task})"""

#СBV Update

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/project_update.html'
    pk_url_kwarg = 'project_id'
    success_url = reverse_lazy('tasks:projects_list')
    
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    pk_url_kwarg = 'task_id'

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail', kwargs={'project_id': self.object.project.id, 'task_id': self.object.id})

#FBV Delete
"""
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return redirect('tasks:projects_list')

def delete_task(request, project_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('tasks:project_detail', project_id=project_id)"""

#СBV Delete
class ProjectDeleteView(DeleteView):
    model = Project
    pk_url_kwarg = 'project_id'
    success_url = reverse_lazy('tasks:projects_list')
    template_name = 'tasks/project_confirm_delete.html'

class TaskDeleteView(DeleteView):
    model = Task
    pk_url_kwarg = 'task_id'

    def get_success_url(self):
        return reverse_lazy('tasks:project_detail', kwargs={'project_id': self.object.project.id})