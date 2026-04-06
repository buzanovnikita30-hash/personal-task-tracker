from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.board, name="board"),
    path("tasks/quick-add/", views.quick_add, name="quick_add"),
    path("tasks/move/", views.move_task, name="move"),
    path("tasks/<int:task_id>/", views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/update/", views.task_update, name="task_update"),
    path("tasks/<int:task_id>/archive/", views.task_archive, name="task_archive"),
    path("tasks/<int:task_id>/comment/", views.add_comment, name="add_comment"),
    path("tasks/<int:task_id>/reminder/", views.add_reminder, name="add_reminder"),
]

