from .models import Task
from .serializer import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404


class TaskListCreate(APIView):
    def get(self, request):
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response({'tasks': serializer.data})

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response({'id': task.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

