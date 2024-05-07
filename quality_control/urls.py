from django.urls import path, include
from . import views

app_name = 'quality_control'

urlpatterns = [
    #path('', views.index, name='index'), 
    #path('features/', views.feature_list, name='feature_list'), 
    path('', views.IndexView.as_view(), name='index'),
    path('bugs/', views.bug_list, name='bug_list'), 
    path('features/', views.feature_list, name='feature_list'), 
    path('bugs/<int:bug_id>/', views.BugDetailView.as_view(), name='bug_detail'),
    path('features/<int:feature_id>/', views.FeatureDetailView.as_view(), name='feature_detail'),
    #path('bugs/new/', views.create_bug_report, name='create_bug_report'),
    #path('features/new/', views.create_feature_request, name='create_feature_request'),
    path('bugs/create_bug_report/', views.BugReportCreateView.as_view(), name='create_bug_report'),
    path('bugs/create_feature_request/', views.FeatureRequestCreateView.as_view(), name='create_feature_request'),
    path('bugs/<int:bug_id>/update_bug_report/', views.BugReportUpdateView.as_view(), name='update_bug_report'),
    path('features/<int:feature_id>/update_feature_request/', views.FeatureRequestUpdateView.as_view(), name='update_feature_request'),
    #path('bugs/<int:bug_id>/delete/', views.BugReportDeleteView.as_view(), name='delete_bug_report'),
    path('bugs/<int:bug_id>/delete/', views.delete_bug_report, name='delete_bug_report'),
    path('features/<int:feature_id>/delete/', views.delete_feature_request, name='delete_feature_request'),
    
]

