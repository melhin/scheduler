from django.http import JsonResponse
from django.views.generic import View
from http import HTTPStatus

from api.v1.forms import ScheduleForm

from interview.models import Slot


class Schedule(View):

    def get(self, request):

        data = {
                'interviewers': request.GET.getlist('interviewer'),
                'candidate': request.GET.get('candidate'),
        }
        form = ScheduleForm(data)
        if not form.is_valid():
            return JsonResponse({'error': form.errors},
                                status=HTTPStatus.BAD_REQUEST)

        if form.cleaned_data['candidate']:
            print (Slot.objects.get_slots_for_candidate(form.cleaned_data['candidate'],
                specific_users=form.cleaned_data['interviewers']))
        else:
            print (Slot.objects.get_slots_for_interviewers(form.cleaned_data['interviewers']))
        return JsonResponse({'data': 'success'})
