from django.contrib import admin

from .models import ActivityLog, Comment, Reminder, Tag, Task

admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Reminder)
admin.site.register(ActivityLog)

