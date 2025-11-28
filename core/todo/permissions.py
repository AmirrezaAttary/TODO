from django.core.exceptions import PermissionDenied
from .models import Task

class UserIsOwnerMixin:
    """
    پرمیژن برای اینکه فقط صاحب تسک اجازه دسترسی داشته باشد
    """

    def dispatch(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get("pk"))
        if task.user != request.user:  # فرض بر این است که Task یک فیلد user دارد
            raise PermissionDenied("شما اجازه دسترسی به این تسک را ندارید.")
        return super().dispatch(request, *args, **kwargs)
