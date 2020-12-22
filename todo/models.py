from django.db import models
from mylib.base_model import DateAbstract
from users.models import User


class Todo(DateAbstract):
    user = models.ForeignKey(User, related_name="user_todos", on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=50)
    description = models.TextField()
    # image = ProcessedImageField(null=True, blank=True,
    #                                     upload_to=scramble,
    #                                     processors=[ResizeToFill(100, 50)],
    #                                     format='JPEG',
    #                                     options={'quality': 100})
    time_todo = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title
