from django.contrib import admin
import datetime

from .models import BuyerUser, Artist, Label, Item, ItemType
from .utilities import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')


send_activation_notifications.short_description = 'Отправка писем с требованиями активации'

class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более трёх дней'),
            ('week', 'Не прошли более недели')
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)


class BuyerUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (
        ('username', 'email'),
        ('first_name', 'last_name'),
        ('send_notif', 'is_active', 'is_activated'),
        ('is_staff', 'is_superuser'),
        'groups',
        'user_permissions',
        ('last_login', 'date_joined')
    )
    readonly_fields =  ('last_login', 'date_joined')
    actions = (send_activation_notifications,)


class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('album',)}


class LabelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(BuyerUser, BuyerUserAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(ItemType)
