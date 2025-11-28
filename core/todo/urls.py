from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TodoListView.as_view(), name='task-list'),
    path('create', views.TodoCreateView.as_view(), name='task-create'),
    path('complete/<int:pk>', views.TodoCompleteView.as_view(), name="task-complete"),
    path('undone/<int:pk>', views.TodoUndoneView.as_view(), name="task-undone"),
    path('delete/<int:pk>', views.TodoDeleteView.as_view(), name="task-delete"),
    path('edit/<int:pk>', views.TodoUpdateView.as_view(), name='task-update'),
]
