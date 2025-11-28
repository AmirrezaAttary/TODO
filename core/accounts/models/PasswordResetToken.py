import uuid
import hashlib
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reset_tokens")
    token_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)   # ← اضافه کن

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    @staticmethod
    def create_token(user, hours=48):
        import uuid, hashlib
        from django.utils import timezone
        from datetime import timedelta

        raw_token = uuid.uuid4().hex
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        expires_at = timezone.now() + timedelta(hours=hours)

        obj = PasswordResetToken.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=expires_at
        )
        return raw_token, obj

