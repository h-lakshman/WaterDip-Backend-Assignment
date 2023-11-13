from .models import Task
from .serializer import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class TaskList(APIView):
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