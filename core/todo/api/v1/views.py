from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ...models import Task
from .serializers import TaskSerializer
from .paginations import LargeResultsSetPagination
from .permissions import IsOwnerOrReadOnly


class TaskModelViewSet(viewsets.ModelViewSet):
    '''getting a list of tasks and creating new task'''
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['complete']
    search_fields = ['title']
    ordering_fields = ['created_date']
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)