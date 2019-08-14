from django.db import models
from django.utils import timezone

from core.constants import INTERVIEWER
from core.constants import CANDIDATE

from core.models import AbstractTimeStamp
from core.models import UserProfile

from interview.constants import FREE
from interview.constants import BOOKED


class SlotManager(models.Manager):

    def get_interview_slots(self, role, start, end,
                            specific_users=None):
        cross_ref_dct = {
            CANDIDATE: INTERVIEWER,
            INTERVIEWER: CANDIDATE,
        }
        resp = self.get_queryset().\
            select_related('user_profile__user').filter(
                user_profile__role=cross_ref_dct[role],
                status=FREE,
                start__gte=start,
                end__lte=end,
            )
        if specific_users:
            resp = resp.filter(user_profile__in=specific_users)
        return resp

    def get_slots_for_candidate(self, user_profile, specific_users=None):
        """get_slots_for_candidate: Takes a user profile object for a candidate
        and then returns the list of interview combination with interviewer[s]
        information along with the start and end time
        """
        interview_slots = []
        candidate_free_slots = self.get_queryset().\
            select_related('user_profile__user').filter(
                user_profile=user_profile,
                status=FREE,
            )

        for each_slot in candidate_free_slots:
            available_interviewers = self.get_interview_slots(
                user_profile.role,
                each_slot.start,
                each_slot.end,
                specific_users=specific_users,
            )
            # setting interviewer user profile
            interviewer_profile = [ele.user_profile
                                   for ele in available_interviewers]
            if available_interviewers:
                interview_slots.append({
                    'candidate': each_slot,
                    'interviewers': interviewer_profile,
                })
        return interview_slots

    @staticmethod
    def _assign_people(candidates, interviewers):
        """_assign_people: Assign candidates and interviewers equally amongst
        interviewers
        """
        tmp_intvs = list(interviewers)
        grps = {}
        i = 0
        while tmp_intvs:
            try:
                can = candidates[i]
            except IndexError:
                i = 0
                can = candidates[i]
            grps.setdefault(can, []).append(tmp_intvs.pop(0))
            i += 1

        slots = []
        for slot, intvs in grps.items():
            slots.append({
                'candidate': slot,
                'interviewers': intvs,
            })
        return slots

    def get_slots_for_interviewers(self, user_profiles):
        """get_slots_for_interviewer: Takes a list of user profile objects for
        a interviewers then returns the list of interview combination with
        candidate
        """
        interview_slots = []
        slots = {}

        # Get all the slots for user_profiles given
        for ele in Slot.objects.filter(user_profile__in=user_profiles)\
                .values():
            slots.setdefault(ele['start'], []).append(ele)

        # filter only slots that have all the user profiles involved
        selected_slots = [
            val
            for _, val in slots.items()
            if len(user_profiles) == len(val)
        ]

        for slots in selected_slots:
            candidates = self.get_interview_slots(INTERVIEWER,
                                                  slots[0]['start'],
                                                  slots[0]['end'])
            interview_slots.extend(self._assign_people(candidates,
                                                       user_profiles))
        return interview_slots


class Slot(AbstractTimeStamp):
    STATUS = (
        (FREE, 'Free'),
        (BOOKED, 'Booked')
    )
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=2, default=FREE, choices=STATUS)
    objects = SlotManager()

    def mark_booked(self):
        self.status = BOOKED
        self.save()

    def save(self, *args, **kwargs):
        """Overiding save so that we have the end set to one hour even from the admin
        """
        if self.start:
            self.end = self.start + timezone.timedelta(hours=1)
        return super(Slot, self).save(*args, **kwargs)

    def __str__(self):
        return '{user_profile}:{status}'.format(
            user_profile=self.user_profile,
            status=self.status,
        )
