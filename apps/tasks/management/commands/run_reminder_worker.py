import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.tasks.models import Reminder
from apps.tasks.services import log_change

logger = logging.getLogger("apps.tasks")


class Command(BaseCommand):
    help = "Отправляет ожидающие напоминания (режим in-app логирования)."

    def handle(self, *args, **options):
        now = timezone.now()
        reminders = Reminder.objects.filter(is_active=True, sent_at__isnull=True, remind_at__lte=now).select_related("task")
        count = 0
        for reminder in reminders:
            reminder.sent_at = now
            reminder.save(update_fields=["sent_at"])
            log_change(reminder.task, "reminder_sent", "remind_at", "", reminder.remind_at)
            logger.info("Reminder sent for task_id=%s at=%s", reminder.task_id, reminder.remind_at.isoformat())
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Обработано напоминаний: {count}"))

