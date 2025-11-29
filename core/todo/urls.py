from django.urls import path,include
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TodoListView.as_view(), name='task-list'),
    path('create', views.TodoCreateView.as_view(), name='task-create'),
    path('complete/<int:pk>', views.TodoCompleteView.as_view(), name="task-complete"),
    path('undone/<int:pk>', views.TodoUndoneView.as_view(), name="task-undone"),
    path('delete/<int:pk>', views.TodoDeleteView.as_view(), name="task-delete"),
    path('edit/<int:pk>', views.TodoUpdateView.as_view(), name='task-update'),
    path('weatherview/',views.weather_view,name='weather_view'),
    path('api/v1/',include('todo.api.v1.urls')),
]
