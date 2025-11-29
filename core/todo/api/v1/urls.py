from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 

app_name = 'api-v1'
router = DefaultRouter()
router.register('task',views.TaskModelViewSet,basename='task')
urlpatterns = [
    path('weather/', views.WeatherAPIView.as_view(), name='weather-default'),
    path('weather/<str:city>/', views.WeatherAPIView.as_view(), name='weather-city'),
]
urlpatterns += router.urls
