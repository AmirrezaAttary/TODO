from django.urls import path, include
from todo.api.v1 import views 
from rest_framework.routers import DefaultRouter

app_name = 'api-v1'
router = DefaultRouter()
router.register('task',views.TaskModelViewSet,basename='task')

urlpatterns = router.urls
