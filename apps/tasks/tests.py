from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Reminder, Task, TaskPriority, TaskStatus


class TaskModelTests(TestCase):
    def test_overdue(self):
        task = Task.objects.create(title="A", due_date=timezone.localdate() - timedelta(days=1))
        self.assertTrue(task.is_overdue)

    def test_done_sets_completed(self):
        task = Task.objects.create(title="B", status=TaskStatus.DONE, priority=TaskPriority.P2)
        task.mark_done_timestamp()
        self.assertIsNotNone(task.completed_at)


class TaskViewTests(TestCase):
    def test_quick_add_creates_task(self):
        response = self.client.post(reverse("tasks:quick_add"), {"title": "Новая задача"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="Новая задача").exists())

    def test_move_task_changes_status(self):
        task = Task.objects.create(title="Move me", status=TaskStatus.INBOX, board_position=1000)
        response = self.client.post(
            reverse("tasks:move"),
            {"task_id": task.id, "status": TaskStatus.IN_PROGRESS, "position": "2000"},
        )
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)


class ReminderFormFlowTests(TestCase):
    def test_add_future_reminder(self):
        task = Task.objects.create(title="Reminder task")
        remind_at = (timezone.localtime() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M")
        response = self.client.post(reverse("tasks:add_reminder", args=[task.id]), {"remind_at": remind_at})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reminder.objects.filter(task=task).count(), 1)

