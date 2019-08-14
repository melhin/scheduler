from api.utils import convert_to_epcoh


class SlotSerializer(object):
    """SlotSerializer: is a custom serializer for the nested data structure
    we have for candidate and interviewers. This is raw and
    little more flexible in this case
    """

    def __init__(self, data):
        self.data = data

    @staticmethod
    def _serialize_candidate(slot):
        return {
            'name': slot.user_profile.user.first_name,
            'email': slot.user_profile.user.email,
            'start': convert_to_epcoh(slot.start),
            'end': convert_to_epcoh(slot.end),
        }

    def serialize(self):
        resp = []
        for ele in self.data:
            slot = {}
            slot['candidate'] = self._serialize_candidate(ele['candidate'])
            for interviewer in ele['interviewers']:
                tmp = {
                    'email': interviewer.user.email,
                    'name': interviewer.user.first_name,
                }
                slot.setdefault('interviewers', []).append(tmp)
            resp.append(slot)
        return resp
