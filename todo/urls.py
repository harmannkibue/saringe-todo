from django.conf.urls import url
from .views import ListCreateTodo, RetrieveUpdateDestroyTodo

urlpatterns = [
    url(r'^create-todo/$', ListCreateTodo.as_view(), name="create_todo"),
    url(r'^(?P<pk>[0-9]+)/?$', RetrieveUpdateDestroyTodo.as_view(), name="retrieve_update_destroy_todo"),
]
