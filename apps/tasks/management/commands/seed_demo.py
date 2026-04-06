from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.tasks.models import Tag, Task, TaskPriority, TaskStatus


class Command(BaseCommand):
    help = "Create demo tasks for first run."

    def handle(self, *args, **options):
        if Task.objects.exists():
            self.stdout.write(self.style.WARNING("Задачи уже существуют, сид пропущен."))
            return

        home = Tag.objects.create(name="Дом", color="#60a5fa")
        work = Tag.objects.create(name="Работа", color="#a78bfa")
        health = Tag.objects.create(name="Здоровье", color="#34d399")

        tasks = [
            Task(title="Разобрать входящие идеи", status=TaskStatus.INBOX, priority=TaskPriority.P3, board_position=1000),
            Task(
                title="Запланировать неделю",
                status=TaskStatus.PLANNED,
                priority=TaskPriority.P2,
                due_date=timezone.localdate(),
                board_position=1000,
            ),
            Task(title="Сделать тренировку", status=TaskStatus.IN_PROGRESS, priority=TaskPriority.P1, board_position=1000),
            Task(title="Жду ответ от банка", status=TaskStatus.WAITING, priority=TaskPriority.P2, board_position=1000),
        ]
        for task in tasks:
            task.save()
        tasks[0].tags.add(work)
        tasks[1].tags.add(work)
        tasks[2].tags.add(health)
        tasks[3].tags.add(home)

        self.stdout.write(self.style.SUCCESS("Демо-данные созданы."))

