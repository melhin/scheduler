from django.db import models

from core.models import AbstractTimeStamp
from core.models import UserProfile


class SlotManager(models.Manager):

    def get_canditate_slots(self):
        return self.get_queryset().filter(
            user_profile__role='CA',
            status='F',
            start__gte=self.start,
            end__lte=self.end,
        )

    def get_interviewer_slots(self):
        return self.get_queryset().filter(
            user_profile__role='IN',
            status='F',
            start__gte=self.start,
            end__lte=self.end,
        )


class Slot(AbstractTimeStamp):
    STATUS = (
        ('F', 'Free'),
        ('B', 'Booked')
    )
    user_profile = UserProfile
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=2, default='F', choices=STATUS)
    objects = SlotManager()

    def mark_booked(self):
        self.status = 'B'
        self.save()
