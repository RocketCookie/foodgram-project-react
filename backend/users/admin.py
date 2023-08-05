from django.contrib import admin

from users.models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )

    list_editable = ('role',)
    search_fields = ('email', 'username')
    list_filter = ('role',)
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'subscribing')
    list_editable = ('user', 'subscribing')
    empty_value_display = '-пусто-'
