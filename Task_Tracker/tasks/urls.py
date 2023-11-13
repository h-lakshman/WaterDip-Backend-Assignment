from django.urls import path
from .views import TaskListCreate, TaskDetail, bulk_add_tasks, bulk_delete_tasks

urlpatterns = [
    path('tasks/', TaskListCreate.as_view()),
    path('tasks/<int:id>', TaskDetail.as_view()),
    # path('tasks/bulk_add_tasks',bulk_add_tasks),
    # path('tasks/bulk_delete_tasks',bulk_add_tasks),
]
