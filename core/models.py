import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone

from core.constants import CANDIDATE
from core.constants import INTERVIEWER


class AbstractTimeStamp(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(AbstractTimeStamp, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class User(AbstractUser):
    """User: will contain just a uuid field for now
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class UserProfile(AbstractTimeStamp):
    """UserProfile: Will have all the attributes related to the user
    like Role, education, qualification e.tc.
    """
    ROLES = (
        (INTERVIEWER, 'Interviewer'),
        (CANDIDATE, 'Candidate')

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=4, choices=ROLES)

    def __str__(self):
        return '{user}:{role}'.format(user=self.user, role=self.role)
