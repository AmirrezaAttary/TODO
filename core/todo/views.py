import requests
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.conf import settings
from .models import Task
from .forms import TodoUpdateForm
from .permissions import UserIsOwnerMixin

# Create your views here.

class TodoListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    ordering = "-created_date"
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class TodoCreateView(LoginRequiredMixin,CreateView):
    model = Task
    fields = ["title"]
    success_url = "/"
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreateView, self).form_valid(form)
    
class TodoCompleteView(LoginRequiredMixin,UserIsOwnerMixin,View):
    model = Task
    success_url = "/"

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.complete = True
        object.save()
        return redirect(self.success_url)
    
    
    
class TodoUndoneView(LoginRequiredMixin,UserIsOwnerMixin,View):
    model = Task
    success_url = "/"

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.complete = False
        object.save()
        return redirect(self.success_url)    

    
class TodoDeleteView(LoginRequiredMixin,UserIsOwnerMixin,DeleteView):
    model = Task
    success_url = "/"

class TodoUpdateView(LoginRequiredMixin,UserIsOwnerMixin,UpdateView):
    model = Task
    form_class = TodoUpdateForm
    success_url = "/"


@cache_page(60 * 20)  # کش کردن پاسخ به مدت ۲۰ دقیقه
def weather_view(request, city="تهران"):
    api_key = settings.OPENWEATHER_API_KEY  # از settings یا مستقیماً کلید را قرار دهید
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fa'
    response = requests.get(url)
    
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
        return JsonResponse(result)
    else:
        return JsonResponse({'error': 'شهر یافت نشد'}, status=404)