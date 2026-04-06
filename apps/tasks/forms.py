from django import forms
from django.utils import timezone

from .models import Comment, Reminder, Tag, Task


class QuickTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title"]
        labels = {"title": ""}
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Быстро добавить задачу... (Enter)", "class": "w-full rounded-xl border p-3"}
            )
        }


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "due_date", "due_time", "tags"]
        labels = {
            "title": "Название",
            "description": "Описание",
            "status": "Статус",
            "priority": "Приоритет",
            "due_date": "Дата дедлайна",
            "due_time": "Время дедлайна",
            "tags": "Теги",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "w-full rounded-lg border p-2"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "w-full rounded-lg border p-2"}),
            "status": forms.Select(attrs={"class": "w-full rounded-lg border p-2"}),
            "priority": forms.Select(attrs={"class": "w-full rounded-lg border p-2"}),
            "due_date": forms.DateInput(attrs={"type": "date", "class": "w-full rounded-lg border p-2"}),
            "due_time": forms.TimeInput(attrs={"type": "time", "class": "w-full rounded-lg border p-2"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {"body": ""}
        widgets = {"body": forms.Textarea(attrs={"rows": 2, "placeholder": "Комментарий...", "class": "w-full rounded-lg border p-2"})}


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["remind_at"]
        labels = {"remind_at": ""}
        widgets = {
            "remind_at": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local", "class": "w-full rounded-lg border p-2"},
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["remind_at"].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean_remind_at(self):
        remind_at = self.cleaned_data["remind_at"]
        if timezone.is_naive(remind_at):
            remind_at = timezone.make_aware(remind_at, timezone.get_current_timezone())
        if remind_at <= timezone.now():
            raise forms.ValidationError("Напоминание должно быть в будущем.")
        return remind_at

