from django import forms
from django.core.validators import validate_email
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from api.utils import convert_to_timestamp
from core.models import UserProfile
from interview.models import Slot


class MultiEmailField(forms.Field):

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)
        if value:
            for email in value:
                validate_email(email)


class ScheduleForm(forms.Form):
    candidate = forms.EmailField(required=False)
    interviewers = MultiEmailField(required=False)

    def clean_candidate(self):
        data = self.cleaned_data['candidate']
        user_profile = UserProfile.objects.filter(user__email=data).first()
        if data and not user_profile:
            raise forms.ValidationError(
                _('Candidate %(email)s not found'),
                params={'email': data},
                code='invalid',
            )
        return user_profile

    def clean_interviewers(self):
        intvs = self.cleaned_data['interviewers'] or []
        data = []
        for intv in intvs:
            user_profile = UserProfile.objects.filter(user__email=intv).first()
            if not user_profile:
                raise forms.ValidationError(
                    _('Interviewer %(email)s not found'),
                    params={'email': intv},
                    code='invalid',
                )
            else:
                data.append(user_profile)
        return data

    def clean(self):
        cleaned_data = super(ScheduleForm, self).clean()
        if not any([
            cleaned_data.get('candidate'),
            cleaned_data.get('interviewers'),
        ]):
            raise forms.ValidationError(_('Either candidates or interiewers '
                                          'are required.'))


class SubmitSlotForm(forms.Form):
    user = forms.CharField(required=True)
    start = forms.IntegerField(required=True)

    def clean_start(self):
        start = self.cleaned_data['start']
        start = convert_to_timestamp(start)
        if start <= timezone.now():
            raise forms.ValidationError(_('Slot date should be greater '
                                        'than current date'))
        user_profile = self.cleaned_data['user_profile']
        booked_slot = Slot.objects.filter(
            user_profile=user_profile,
            start__range=[
                start - timezone.timedelta(hours=1),
                start
            ],
        ).exists()
        if booked_slot:
            raise forms.ValidationError(_('User has a slot already booked '
                                          'at this time'))
        return start

    def clean_user(self):
        user = self.cleaned_data['user']
        try:
            self.cleaned_data['user_profile'] = UserProfile.objects.\
                get(user_id=user)
        except UserProfile.DoesNotExist:
            raise forms.ValidationError(_('User Profile does '
                                          'not exist for user'))
        return user

    def save(self):
        Slot.objects.create(user_profile=self.cleaned_data['user_profile'],
                            start=self.cleaned_data['start'])
