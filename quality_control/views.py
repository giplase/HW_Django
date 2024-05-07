from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from .models import BugReport, FeatureRequest
from django.views.generic import ListView, DetailView, CreateView
from django.template.loader import render_to_string
from .forms import BugReportForm, FeatureRequestForm
from django.views.generic.edit import UpdateView, DeleteView



#FBV version 1

"""def index(request):
    bug_list_url = reverse('quality_control:bug_list')
    feature_list_url = reverse('quality_control:feature_list')
    html = f"<h1>Система контроля качества</h1><a href='{bug_list_url}'>Список всех багов</a><br/><a href='{feature_list_url}'>Запросы на улучшение</a>"

    return HttpResponse(html)

def bug_detail(request, id: str):
    id = int(id)
    html = f"<a>Детали бага {id}</a>"
    return HttpResponse(html)

def feature_id_detail(request, id: str):
        id = int(id)
        html = f"<a>Детали улучшения {id}</a>"
        return HttpResponse(html)
"""

#FBV + CBV version 1

"""
class IndexView(View):
    def get(self, request, *args, **kwargs):
        bug_list_url = reverse('quality_control:bug_list')
        feature_list_url = reverse('quality_control:feature_list')
        html = f"<h1>Система контроля качества</h1><a href='{bug_list_url}'>Список всех багов</a><br/><a href='{feature_list_url}'>Запросы на улучшение</a>"
        return HttpResponse(html)

def bug_list(request):
    bugs = BugReport.objects.all()
    bugs_html = '<h1>Cписок отчетов об ошибках</h1><ul>'
    for bug in bugs:
        bugs_html += f'<li><a href="{bug.id}/">{bug.title}. Статус:{bug.status}</br></a></li>'
    bugs_html += '</ul>'
    return HttpResponse(bugs_html)


class BugDetailView(DetailView):
    model = BugReport
    pk_url_kwarg = 'bug_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        bug = self.get_object()
        response_html = f'<h1>{bug.title}</h1><p>{bug.description}<br/>Статус: {bug.status}<br/>Приоритет: {bug.priority}<br/>Проект: {bug.project.name}<br/>Задача: {bug.task.name}</p>'
        return HttpResponse(response_html)

def feature_list(request):
    features = FeatureRequest.objects.all()
    features_html = '<h1>Список запросов на улучшение</h1><ul>'
    for feature in features:
        features_html += f'<li><a href="{feature.id}/">{feature.title}. Статус: {feature.status}</br></a></li>'
    features_html += '</ul>'
    return HttpResponse(features_html)

class FeatureDetailView(DetailView):
    model = FeatureRequest
    pk_url_kwarg = 'feature_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        feature = self.get_object()
        response_html = f'<h1>{feature.title}</h1><p>{feature.description}<br/>Статус: {feature.status}<br/>Приоритет: {feature.priority}<br/>Проект: {feature.project.name}<br/>Задача: {feature.task.name}</p>'
        return HttpResponse(response_html)
"""

#FBV + CBV version 2

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'quality_control/index.html')

def bug_list(request):
    bugs = BugReport.objects.all()
    return render(request, 'quality_control/bug_list.html', {'bug_list': bugs})

class BugDetailView(DetailView):
    model = BugReport
    pk_url_kwarg = 'bug_id'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        bug = self.get_object()
        return render(request, 'quality_control/bug_detail.html',{'bug':bug})
    
def feature_list(request):
    features = FeatureRequest.objects.all()
    return render(request, 'quality_control/feature_list.html', {'feature_list': features})

class FeatureDetailView(DetailView):
    model = FeatureRequest
    pk_url_kwarg = 'feature_id'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        feature = self.get_object()
        return render(request, 'quality_control/feature_detail.html',{'feature':feature})

#FBV create
"""
def create_bug_report(request):
    if request.method == 'POST':
        form = BugReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quality_control:bug_list')
    else:
        form = BugReportForm()
    return render(request, 'quality_control/bug_report_form.html', {'form': form})

def create_feature_request(request):
    if request.method == 'POST':
        form = FeatureRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quality_control:feature_list')
    else:
        form = FeatureRequestForm()
    return render(request, 'quality_control/feature_request_form.html', {'form': form})"""

#CBV create
class BugReportCreateView(CreateView):
    model = BugReport
    form_class = BugReportForm
    template_name = 'quality_control/bug_report_form.html'
    success_url = reverse_lazy('quality_control:bug_list')

class FeatureRequestCreateView(CreateView):
    model = FeatureRequest
    form_class = FeatureRequestForm
    template_name = 'quality_control/feature_request_form.html'
    success_url = reverse_lazy('quality_control:feature_list')

#FBV update
"""
def update_bug_report(request, bug_id):
    bug_report = get_object_or_404(BugReport, pk=bug_id)
    if request.method == 'POST':
        form = BugReportForm(request.POST, instance=bug)
        if form.is_valid():
            form.save()
            return redirect('quality_control:bug_list', bug_id=bug.id)
    else:
        form = BugReportForm(instance=bug)
    return render(request, 'quality_control/bug_report_update.html', {'form': form, 'bug': bug})"""

#CBV update
class BugReportUpdateView(UpdateView):
    model = BugReport
    form_class = BugReportForm
    template_name = 'quality_control/bug_report_update.html'
    pk_url_kwarg = 'bug_id'
    success_url = reverse_lazy('quality_control:bug_list')

class FeatureRequestUpdateView(UpdateView):
    model = FeatureRequest
    form_class = FeatureRequestForm
    template_name = 'quality_control/feature_request_update.html'
    pk_url_kwarg = 'feature_id'
    success_url = reverse_lazy('quality_control:feature_list')

#СBV delete
"""
class BugReportDeleteView(DeleteView):
    model = BugReport
    pk_url_kwarg = 'bug_id'
    success_url = reverse_lazy('quality_control:bug_list')
    template_name = 'quality_control/bug_report_confirm_delete.html'"""

#FBV delete

def delete_bug_report(request, bug_id):
    bug = get_object_or_404(BugReport, pk=bug_id)
    bug.delete()
    return redirect('quality_control:bug_list')

def delete_feature_request(request, feature_id):
    feature = get_object_or_404(FeatureRequest, pk=feature_id)
    feature.delete()
    return redirect('quality_control:feature_list')


    