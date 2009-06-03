from django.db import models
from schedule.models import Event

class Club(models.Model):
    name = models.CharField('name', max_length = 200)
    description = models.CharField('description', max_length = 2000)
    
    def __unicode__(self):
            return u'%d' % self.id

class ClubMeeting(Event):
    club = models.ForeignKey(Club, related_name = "meetings")
    place = models.CharField('place', max_length = 200)
