from django.urls import path
from .views import TaskListCreate, TaskDetail

urlpatterns = [
    path('tasks/', TaskListCreate.as_view()),
    path('tasks/<int:id>', TaskDetail.as_view())
]
