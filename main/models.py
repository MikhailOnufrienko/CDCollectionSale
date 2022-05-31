from django.db import models
from django.contrib.auth.models import AbstractUser


class BuyerUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Активирован')
    send_notif = models.BooleanField(default=True, db_index=True, verbose_name='Посылать уведомления')

    class Meta(AbstractUser.Meta):
        pass


class Artist(models.Model):
    name = models.CharField(max_length=64, verbose_name='Исполнитель')
    country = models.CharField(max_length=32, null=True, blank=True, verbose_name='Страна')

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
        ordering = ['name']

    def __str__(self):
        return self.name


class ItemType(models.Model):
    class Types(models.TextChoices):
        CD = 'CD', 'CD'
        DOUBLE_CD = '2xCD', '2xCD'
        CD_DIGIPAK = 'CD Digipak', 'CD Digipak'
        DOUBLE_CD_DIGIPAK = '2xCD Digipak', '2xCD Digipak'
        DVD = 'DVD', 'DVD'
        DOUBLE_DVD = '2xDVD', '2xDVD'
        DVD_DIGIPAK = 'DVD Digipak', 'DVD Digipak'
        DOUBLE_DVD_DIGIPAK = '2xDVD Digipak', '2xDVD Digipak'
    format = models.CharField(max_length=16, choices=Types.choices, default=Types.CD, verbose_name='Формат')

    class Meta:
        verbose_name = 'Формат'
        verbose_name_plural = 'Форматы'

    def __str__(self):
        return self.format


class Label(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Лейбл'
        verbose_name_plural = 'Лейблы'

    def __str__(self):
        return self.name


class Item(models.Model):
    item_type = models.ForeignKey(ItemType, on_delete=models.PROTECT)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    album = models.CharField(max_length=128, verbose_name='Альбом')
    label = models.ForeignKey(Label, related_name='items', on_delete=models.PROTECT)
    licensed_by = models.ForeignKey(Label, null=True, blank=True, on_delete=models.PROTECT)
    year = models.CharField(max_length=4)
    license_year = models.CharField(max_length=4, null=True, blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товар'

    def __str__(self):
        return self.album
