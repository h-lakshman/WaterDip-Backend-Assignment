from .models import Task
from .serializer import TaskSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

# This class-based view performs Listing and Creation of Tasks


class TaskListCreate(APIView):
    def get(self, request):
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        return Response({'tasks': serializer.data})

    def post(self, request):
        if 'tasks' in request.data: # This condition bulk add tasks
            tasks = request.data.get('tasks', [])
            created_tasks = []

            for task in tasks:
                serializer = TaskSerializer(data=task)
                if serializer.is_valid():
                    task_save = serializer.save()
                    created_tasks.append({'id': task_save.id})

            return Response({'tasks': created_tasks}, status=status.HTTP_201_CREATED)

        else: #This condition adds 1 task
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                task = serializer.save()
                return Response({'id': task.id}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if 'tasks' in request.data: #This condition bulk deletes tasks
            tasks_data = request.data.get('tasks', [])

            for task_data in tasks_data:
                task_id = task_data.get('id', None)
                if task_id is not None:
                    try:
                        task = Task.objects.get(pk=task_id)
                        task.delete()
                    except Task.DoesNotExist:  # If handle doesnt exist, it does nothing
                        pass  

            return Response(status=status.HTTP_204_NO_CONTENT)

# This class-based view performs getting a particular task,editing and deleting the task
class TaskDetail(APIView):
    def get(self, request, id):
        try:
            task = get_object_or_404(Task, id=id)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Http404:
            return Response({'error': 'There is no task at that id'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            task = get_object_or_404(Task, id=id)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({'error': 'There is no task at that id'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            task = get_object_or_404(Task, id=id)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'error': 'There is no task at that id'}, status=status.HTTP_404_NOT_FOUND)



# @api_view(['POST'])
# def bulk_add_tasks(request):
#     tasks = request.data.get('tasks', [])
#     created_tasks = []

#     for task in tasks:
#         serializer = TaskSerializer(data=task)
#         if serializer.is_valid():
#             task_save = serializer.save()
#             created_tasks.append({'id': task_save.id})

#     return Response({'tasks': created_tasks}, status=status.HTTP_201_CREATED)


# # This function-based view is used to bulk delete tasks
# @api_view(['DELETE'])
# def bulk_delete_tasks(request):
#     tasks = request.data.get('tasks', [])

#     for task in tasks:
#         task_id = task.get('id', None)
#         if task_id is not None:
#             try:
#                 task_del = Task.objects.get(pk=task_id)
#                 task_del.delete()
#             except Task.DoesNotExist: 
#                 pass

#     return Response(status=status.HTTP_204_NO_CONTENT)
