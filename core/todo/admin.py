from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id","title", "user", "complete", "created_date", "updated_date")
    list_filter = ("complete", "user")
    search_fields = ("title", "user__username")
    list_editable = ("complete",)
    ordering = ("-created_date",)

    # نمایش بهتر فرم داخل صفحه ویرایش
    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": ("title", "user")
        }),
        ("وضعیت", {
            "fields": ("complete",)
        }),
        ("تاریخ‌ها (غیرقابل ویرایش)", {
            "fields": ("created_date", "updated_date"),
            "classes": ("collapse",)
        }),
    )

    readonly_fields = ("created_date", "updated_date")
