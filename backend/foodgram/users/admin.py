from django.contrib import admin
from .models import User, Subscriptions


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email',)


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author',)
    search_fields = ('user__username', 'author__username',)
    list_filter = ('user__username', 'author__username',)
