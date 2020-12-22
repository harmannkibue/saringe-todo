from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50, required=True, allow_blank=False)
    description = serializers.CharField(max_length=300, required=True, allow_blank=False)
    time_todo = serializers.DateTimeField(required=True)

    class Meta:
        model = Todo
        fields = ('title', 'description', 'time_todo')


class RetrieveUpdateDestroyTodoSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=False, allow_blank=True)
    description = serializers.CharField(max_length=300, required=False, allow_blank=True)
    time_todo = serializers.DateTimeField(required=False)

    class Meta:
        model = Todo
        fields = ('title', 'description', 'time_todo')
