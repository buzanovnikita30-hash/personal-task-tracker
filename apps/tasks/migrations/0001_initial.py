from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=32, unique=True)),
                ("color", models.CharField(default="#94a3b8", max_length=7)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("description", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("inbox", "Inbox"), ("planned", "Planned"), ("in_progress", "In Progress"), ("waiting", "Waiting"), ("done", "Done")], default="inbox", max_length=24)),
                ("priority", models.CharField(choices=[("p1", "P1 Critical"), ("p2", "P2 High"), ("p3", "P3 Normal"), ("p4", "P4 Low")], default="p3", max_length=4)),
                ("due_date", models.DateField(blank=True, null=True)),
                ("due_time", models.TimeField(blank=True, null=True)),
                ("board_position", models.DecimalField(decimal_places=4, default=1000, max_digits=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("archived_at", models.DateTimeField(blank=True, null=True)),
                ("tags", models.ManyToManyField(blank=True, related_name="tasks", to="tasks.tag")),
            ],
            options={"ordering": ["status", "board_position", "-updated_at"]},
        ),
        migrations.CreateModel(
            name="Reminder",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("remind_at", models.DateTimeField()),
                ("sent_at", models.DateTimeField(blank=True, null=True)),
                ("channel", models.CharField(default="in_app", max_length=16)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("task", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reminders", to="tasks.task")),
            ],
            options={"ordering": ["remind_at"]},
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("task", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="tasks.task")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ActivityLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(max_length=64)),
                ("field_name", models.CharField(blank=True, max_length=64)),
                ("old_value", models.TextField(blank=True)),
                ("new_value", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("task", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="activity", to="tasks.task")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(model_name="task", index=models.Index(fields=["status", "board_position"], name="tasks_task_status__27397f_idx")),
        migrations.AddIndex(model_name="task", index=models.Index(fields=["due_date"], name="tasks_task_due_dat_18435b_idx")),
        migrations.AddIndex(model_name="task", index=models.Index(fields=["priority"], name="tasks_task_priorit_894fdf_idx")),
        migrations.AddIndex(model_name="task", index=models.Index(fields=["archived_at"], name="tasks_task_archive_393904_idx")),
        migrations.AddIndex(model_name="reminder", index=models.Index(fields=["is_active", "sent_at", "remind_at"], name="tasks_remind_is_acti_b26fe1_idx")),
    ]

