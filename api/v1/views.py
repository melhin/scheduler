from http import HTTPStatus

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.v1.forms import SubmitSlotForm
from api.v1.forms import ScheduleForm
from api.v1.serializers import SlotSerializer


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
        user = self.request.user.id
        start = self.request.data.get('start')
        form = SubmitSlotForm({'user': user, 'start': start})
        if form.is_valid():
            form.save()
            response = Response({'status': 'success'})
        else:
            response = Response({'status': 'fail', 'error': form.errors},
                                status=HTTPStatus.BAD_REQUEST)
        return response
