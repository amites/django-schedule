from django import forms
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from schedule_tests.models import Club, ClubMeeting
from schedule.forms import SpanForm

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ('name', 'description')

class MeetingForm(SpanForm):
    club = forms.ModelChoiceField(queryset=Club.objects.all(),
            widget=forms.HiddenInput())

    class Meta:
        model = ClubMeeting
        fields = ('place', 'start', 'end')
