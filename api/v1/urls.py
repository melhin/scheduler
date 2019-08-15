from django.urls import path

from api.v1.views import Schedule

urlpatterns = [
    path('schedule/', Schedule.as_view(), name='schedule'),
]
