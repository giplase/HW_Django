from django.contrib import admin
from .models import BugReport, FeatureRequest

# Класс администратора для модели BugReport
@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'project','task')
    search_fields = ('title', 'description')
    list_editable = ('status',)
    fieldsets = (
        (None, {
            'fields': ('title','project', 'description', 'task')
        }),
        ('Availability', {
            'fields': ('status', 'priority')
        }),
    )
    
    
    
# Класс администратора для модели FeatureRequestk
@admin.register(FeatureRequest)
class FeatureRequest(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'project','task')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title','project', 'description', 'task')
        }),
        ('Availability', {
            'fields': ('status','priority')
        }),
    )