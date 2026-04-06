from .models import ActivityLog, Task


def log_change(task: Task, action: str, field_name: str = "", old_value: str = "", new_value: str = ""):
    ActivityLog.objects.create(
        task=task,
        action=action,
        field_name=field_name,
        old_value=str(old_value or ""),
        new_value=str(new_value or ""),
    )

