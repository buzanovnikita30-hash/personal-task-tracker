from django.db import models
from django.utils import timezone


class TaskStatus(models.TextChoices):
    INBOX = "inbox", "Входящие"
    PLANNED = "planned", "Запланировано"
    IN_PROGRESS = "in_progress", "В работе"
    WAITING = "waiting", "Ожидание"
    DONE = "done", "Готово"


class TaskPriority(models.TextChoices):
    P1 = "p1", "P1 Критично"
    P2 = "p2", "P2 Высокий"
    P3 = "p3", "P3 Нормальный"
    P4 = "p4", "P4 Низкий"


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    color = models.CharField(max_length=7, default="#94a3b8")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=24, choices=TaskStatus.choices, default=TaskStatus.INBOX)
    priority = models.CharField(max_length=4, choices=TaskPriority.choices, default=TaskPriority.P3)
    due_date = models.DateField(blank=True, null=True)
    due_time = models.TimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")
    board_position = models.DecimalField(max_digits=12, decimal_places=4, default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    archived_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "board_position"]),
            models.Index(fields=["due_date"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["archived_at"]),
        ]
        ordering = ["status", "board_position", "-updated_at"]

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if not self.due_date or self.status == TaskStatus.DONE:
            return False
        return self.due_date < timezone.localdate()

    @property
    def is_today(self):
        return self.due_date == timezone.localdate()

    def mark_done_timestamp(self):
        if self.status == TaskStatus.DONE and not self.completed_at:
            self.completed_at = timezone.now()
        if self.status != TaskStatus.DONE:
            self.completed_at = None


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Reminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="reminders")
    remind_at = models.DateTimeField()
    sent_at = models.DateTimeField(blank=True, null=True)
    channel = models.CharField(max_length=16, default="in_app")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["is_active", "sent_at", "remind_at"])]
        ordering = ["remind_at"]


class ActivityLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="activity")
    action = models.CharField(max_length=64)
    field_name = models.CharField(max_length=64, blank=True)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    ACTION_LABELS = {
        "created": "Задача создана",
        "status_changed": "Статус изменен",
        "priority_changed": "Приоритет изменен",
        "due_date_changed": "Срок изменен",
        "comment_added": "Добавлен комментарий",
        "reminder_added": "Добавлено напоминание",
        "reminder_sent": "Напоминание отправлено",
        "archived": "Задача архивирована",
    }

    FIELD_LABELS = {
        "status": "Статус",
        "priority": "Приоритет",
        "due_date": "Дата",
        "remind_at": "Напомнить в",
    }

    def action_label(self):
        return self.ACTION_LABELS.get(self.action, self.action)

    def field_label(self):
        return self.FIELD_LABELS.get(self.field_name, self.field_name)

    def _display_value(self, value):
        status_map = {key: label for key, label in TaskStatus.choices}
        priority_map = {key: label for key, label in TaskPriority.choices}
        if value in status_map:
            return status_map[value]
        if value in priority_map:
            return priority_map[value]
        return value

    def old_value_label(self):
        return self._display_value(self.old_value)

    def new_value_label(self):
        return self._display_value(self.new_value)

