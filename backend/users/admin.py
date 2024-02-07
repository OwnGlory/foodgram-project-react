from django.contrib import admin

from users.models import MyUser


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email')


admin.site.register(MyUser, UserAdmin)
