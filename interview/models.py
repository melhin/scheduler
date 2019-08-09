from django.db import models

from core.models import AbstractTimeStamp
from core.models import UserProfile


class SlotManager(models.Manager):

    def get_interview_slots(self, role, start, end):
        cross_ref_dct = {
            'CA': 'IN',
            'IN': 'CA',
        }
        return self.get_queryset().filter(
            user_profile__role=cross_ref_dct[role],
            status='F',
            start__gte=start,
            end__lte=end,
        )


class Slot(AbstractTimeStamp):
    STATUS = (
        ('F', 'Free'),
        ('B', 'Booked')
    )
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=2, default='F', choices=STATUS)
    objects = SlotManager()

    def mark_booked(self):
        self.status = 'B'
        self.save()

    def __str__(self):
        return '{user_profile}:{status}'.format(user_profile=self.user_profile, status=self.status)
