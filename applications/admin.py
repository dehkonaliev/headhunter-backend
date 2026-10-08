from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = ("id", "vacancy", "resume", "status", "created_at",)
    list_filter = ("status",)
    search_fields = ("vacancy__title", "resume__title", "resume__employee__email",)
    raw_id_fields = ("vacancy", "resume",)