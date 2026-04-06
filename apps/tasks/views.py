from decimal import Decimal

from django.db.models import Prefetch, Q
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CommentForm, QuickTaskForm, ReminderForm, TaskForm
from .models import Reminder, Tag, Task, TaskStatus
from .services import log_change


def _apply_filters(queryset, request):
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")
    tag = request.GET.get("tag", "")
    due = request.GET.get("due", "")

    if q:
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if status:
        queryset = queryset.filter(status=status)
    if priority:
        queryset = queryset.filter(priority=priority)
    if tag:
        queryset = queryset.filter(tags__id=tag)
    if due == "today":
        queryset = queryset.filter(due_date=timezone.localdate())
    elif due == "overdue":
        queryset = queryset.filter(due_date__lt=timezone.localdate()).exclude(status=TaskStatus.DONE)
    return queryset.distinct()


def board(request):
    tasks = _apply_filters(Task.objects.filter(archived_at__isnull=True).prefetch_related("tags"), request)
    columns = {
        TaskStatus.INBOX: tasks.filter(status=TaskStatus.INBOX).order_by("board_position"),
        TaskStatus.PLANNED: tasks.filter(status=TaskStatus.PLANNED).order_by("board_position"),
        TaskStatus.IN_PROGRESS: tasks.filter(status=TaskStatus.IN_PROGRESS).order_by("board_position"),
        TaskStatus.WAITING: tasks.filter(status=TaskStatus.WAITING).order_by("board_position"),
    }
    done_count = tasks.filter(status=TaskStatus.DONE).count()
    context = {
        "columns": columns,
        "done_count": done_count,
        "quick_form": QuickTaskForm(),
        "statuses": TaskStatus,
        "tags": Tag.objects.all().order_by("name"),
    }
    return render(request, "tasks/board.html", context)


@require_POST
def quick_add(request):
    form = QuickTaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.board_position = _next_position(task.status)
        task.save()
        log_change(task, "created")
    return redirect("tasks:board")


def task_detail(request, task_id):
    task = get_object_or_404(
        Task.objects.prefetch_related(
            "tags",
            Prefetch("activity"),
            Prefetch("comments"),
            Prefetch("reminders", queryset=Reminder.objects.filter(is_active=True)),
        ),
        pk=task_id,
    )
    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task,
            "form": TaskForm(instance=task),
            "comment_form": CommentForm(),
            "reminder_form": ReminderForm(),
        },
    )


@require_POST
def task_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    old_status = task.status
    old_priority = task.priority
    old_due_date = task.due_date
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
        updated = form.save(commit=False)
        updated.mark_done_timestamp()
        updated.save()
        form.save_m2m()
        if old_status != updated.status:
            log_change(updated, "status_changed", "status", old_status, updated.status)
        if old_priority != updated.priority:
            log_change(updated, "priority_changed", "priority", old_priority, updated.priority)
        if old_due_date != updated.due_date:
            log_change(updated, "due_date_changed", "due_date", old_due_date, updated.due_date)
    return redirect("tasks:task_detail", task_id=task.id)


@require_POST
def task_archive(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.archived_at = timezone.now()
    task.save(update_fields=["archived_at"])
    log_change(task, "archived")
    return redirect("tasks:board")


@require_POST
def add_comment(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.task = task
        comment.save()
        log_change(task, "comment_added")
    return redirect("tasks:task_detail", task_id=task.id)


@require_POST
def add_reminder(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = ReminderForm(request.POST)
    if form.is_valid():
        reminder = form.save(commit=False)
        reminder.task = task
        reminder.channel = "in_app"
        reminder.save()
        log_change(task, "reminder_added", "remind_at", "", reminder.remind_at)
    return redirect("tasks:task_detail", task_id=task.id)


@require_POST
def move_task(request):
    task_id = request.POST.get("task_id")
    status = request.POST.get("status")
    position = request.POST.get("position")
    if not task_id or not status or position is None:
        return HttpResponseBadRequest("Missing fields")
    task = get_object_or_404(Task, pk=task_id)
    if status not in TaskStatus.values:
        return HttpResponseBadRequest("Bad status")
    old_status = task.status
    task.status = status
    task.board_position = Decimal(position)
    task.mark_done_timestamp()
    task.save(update_fields=["status", "board_position", "completed_at", "updated_at"])
    if old_status != status:
        log_change(task, "status_changed", "status", old_status, status)
    return JsonResponse({"ok": True})


def _next_position(status):
    last = Task.objects.filter(status=status).order_by("-board_position").first()
    if not last:
        return Decimal("1000")
    return last.board_position + Decimal("1000")

