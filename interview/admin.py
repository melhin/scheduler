from django.contrib import admin

from interview.models import Slot


class SlotAdmin(admin.ModelAdmin):
    readonly_fields = ['end']


admin.site.register(Slot, SlotAdmin)
