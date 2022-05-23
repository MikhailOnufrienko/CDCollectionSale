from django.db import models
from django.contrib.auth.models import AbstractUser


class BuyerUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Активирован')
    send_notif = models.BooleanField(default=True, db_index=True, verbose_name='Посылать уведомления')

    class Meta(AbstractUser.Meta):
        pass
