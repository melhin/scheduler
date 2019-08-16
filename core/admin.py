from django.contrib import admin

from core.models import User
from core.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(User)
admin.site.register(UserProfile, UserProfileAdmin)
