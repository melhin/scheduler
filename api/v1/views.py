from http import HTTPStatus
from django.utils import timezone

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.v1.forms import ScheduleForm
from api.v1.serializers import SlotSerializer
from api.utils import convert_to_timestamp


from interview.models import Slot


class Schedule(GenericAPIView):

    def get(self, request):
        data = {
                'interviewers': request.GET.getlist('interviewer'),
                'candidate': request.GET.get('candidate'),
        }
        form = ScheduleForm(data)
        if not form.is_valid():
            return Response({'status': 'fail', 'error': form.errors},
                            status=HTTPStatus.BAD_REQUEST)

        if form.cleaned_data['candidate']:
            resp = SlotSerializer(Slot.objects.get_slots_for_candidate(
                form.cleaned_data['candidate'],
                specific_users=form.cleaned_data['interviewers'],
            ))
        else:
            resp = SlotSerializer(Slot.objects.get_slots_for_interviewers(
                form.cleaned_data['interviewers']))
        return Response({'status': 'success', 'data': resp.serialize()})

    def post(self, request):
        user = self.request.user
        start = self.request.data.get('start')
        try:
            start = convert_to_timestamp(start)
        except (TypeError, ValueError):
            return Response({
                'status': 'fail', 'error': 'Slot date not '
                'provided in the right format',
                },
                status=HTTPStatus.BAD_REQUEST)
        if start <= timezone.now():
            return Response({
                'status': 'fail', 'error': 'Slot date should '
                'be greater than current date',
                },
                status=HTTPStatus.BAD_REQUEST)
        Slot.objects.create(user_profile=user.userprofile, start=start)
        return Response({'status': 'success'})
