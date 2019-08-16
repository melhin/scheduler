from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient

from api.utils import convert_to_epoch
from core.models import User
from interview.models import Slot


class ScheduleViewTestCase(TestCase):

    fixtures = ['fixtures/user.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url = reverse('schedule')

        cls.tm_hr = timezone.now().replace(minute=00, second=00,
                                           microsecond=00)
        cls.candidate1 = User.objects.get(email='someone@someone.com')
        Slot.objects.create(user_profile=cls.candidate1.userprofile,
                            start=cls.tm_hr)

        # dummy canidate in the same time slot should not appear in the list
        cls.candidate2 = User.objects.get(email='someone1@someone1.com')
        Slot.objects.create(user_profile=cls.candidate2.userprofile,
                            start=cls.tm_hr)

        cls.interviewer1 = User.objects.get(email='int1@int1.com')
        Slot.objects.create(user_profile=cls.interviewer1.userprofile,
                            start=cls.tm_hr)
        cls.interviewer2 = User.objects.get(email='int2@int2.com')
        Slot.objects.create(user_profile=cls.interviewer2.userprofile,
                            start=cls.tm_hr)

    def test_schedule_retrieving_one_candidate(self):

        # given
        expected = [{'email': 'int1@int1.com', 'name': 'int1'},
                    {'email': 'int2@int2.com', 'name': 'int2'}]

        # when
        client = APIClient()
        client.force_authenticate(user=self.candidate1)
        response = client.get(self.url, {'candidate': self.candidate1.email})
        data = response.data['data']

        # then
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['candidate']['email'], self.candidate1.email)
        self.assertEqual(data[0]['interviewers'], expected)

    def test_schedule_retrieving_interviewer(self):
        """test_schedule_retrieving_interviewer: when given 2 interviewers
        return a list of equally distributed candidates
        """

        # given
        expected1 = [{'email': 'int1@int1.com', 'name': 'int1'}]
        expected2 = [{'email': 'int2@int2.com', 'name': 'int2'}]

        # when
        client = APIClient()
        client.force_authenticate(user=self.interviewer1)
        response = client.get(
            '{url}?interviewer={interviewer1}&interviewer={interviewer2}'.
            format(
                url=self.url,
                interviewer1=self.interviewer1.email,
                interviewer2=self.interviewer2.email,
            )
        )
        data = response.data['data']

        # then
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['candidate']['email'], self.candidate1.email)
        self.assertEqual(data[0]['interviewers'], expected1)
        self.assertEqual(data[1]['candidate']['email'], self.candidate2.email)
        self.assertEqual(data[1]['interviewers'], expected2)

    def test_schedule_retrieving_candidate_without_slots(self):

        client = APIClient()
        client.force_authenticate(user=self.candidate1)
        response = client.get(self.url, {'candidate': 'someone2@someone2.com'})
        data = response.data['data']

        self.assertEqual(len(data), 0)

    def test_schedule_retrieving_candidate_not_in_db(self):

        client = APIClient()
        client.force_authenticate(user=self.candidate1)
        response = client.get(self.url, {'candidate': 'some@some.com'})

        self.assertEqual(response.status_code, 400)

    def test_schedule_retrieving_interviewer_not_in_db(self):

        client = APIClient()
        client.force_authenticate(user=self.candidate1)
        response = client.get(self.url, {'interviewer': 'some@some.com'})

        self.assertEqual(response.status_code, 400)

    def test_schedule_post(self):
        # given
        client = APIClient()
        client.force_authenticate(user=self.candidate1)
        start = convert_to_epoch(self.tm_hr + timezone.timedelta(hours=2))

        # when
        response = client.post(self.url, {'start': start}, format='json')

        # then
        self.assertEqual(response.status_code, 200)

    def test_schedule_post_slot_already_booked(self):
        # given
        client = APIClient()
        client.force_authenticate(user=self.candidate1)
        start = convert_to_epoch(self.tm_hr + timezone.timedelta(hours=2))
        response = client.post(self.url, {'start': start}, format='json')

        # when
        start = convert_to_epoch(self.tm_hr + timezone.timedelta(hours=2,
                                                                 minutes=59))
        response = client.post(self.url, {'start': start}, format='json')

        # then
        self.assertEqual(response.status_code, 400)
