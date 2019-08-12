from django import forms
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

from core.models import UserProfile


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
