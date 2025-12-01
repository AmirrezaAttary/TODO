import requests
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ...models import Task
from .serializers import TaskSerializer
from .paginations import LargeResultsSetPagination
from .permissions import IsOwnerOrReadOnly


class TaskModelViewSet(viewsets.ModelViewSet):
    '''getting a list of tasks and creating new task'''
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['complete']
    search_fields = ['title']
    ordering_fields = ['created_date']

    def get_queryset(self):
        return Task.objects.all()  # برای list و filter

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("شما اجازه دسترسی به این تسک را ندارید")
        return obj
    

# accounts/api/v1/views/weather.py یا هرجایی که ساختار پروژه‌ات است




@method_decorator(cache_page(60 * 20), name='dispatch')  # کش 20 دقیقه
class WeatherAPIView(APIView):
    """
    دریافت وضعیت آب‌وهوا برای یک شهر
    """

    def get(self, request, city="تهران"):
        api_key = settings.OPENWEATHER_API_KEY
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fa'

        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            return Response({'error': 'عدم دسترسی به سرویس خارجی'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if response.status_code == 200:
            data = response.json()
            result = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
            return Response(result)

        return Response({'error': 'شهر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
