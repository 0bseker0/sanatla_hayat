from django.contrib import admin
from .models import Project
from .models import Todo

admin.site.register(Project)

 
class  TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Todo, TodoAdmin)
