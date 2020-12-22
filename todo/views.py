from .models import Todo
from .serializers import TodoSerializer, RetrieveUpdateDestroyTodoSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import pytz

utc = pytz.UTC


class ListCreateTodo(generics.CreateAPIView):
    """This endpoint allows only authenticated users to post a
    todos and admin users to creates and view all todos"""
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = TodoSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=self.request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyTodo(generics.RetrieveUpdateDestroyAPIView):
    """This endpoint allows only authenticated users to get,
    update and delete their todos with the given id in
    the request field"""
    serializer_class = RetrieveUpdateDestroyTodoSerializer
    queryset = Todo.objects.all()
