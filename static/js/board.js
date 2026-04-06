function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
  const columns = document.querySelectorAll(".task-column");
  columns.forEach((col) => {
    new Sortable(col, {
      group: "tasks",
      animation: 180,
      onEnd: async (evt) => {
        const taskId = evt.item.dataset.taskId;
        const status = evt.to.dataset.status;
        const position = (evt.newIndex + 1) * 1000;
        await fetch("/tasks/move/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams({ task_id: taskId, status, position }),
        });
      },
    });
  });
});

