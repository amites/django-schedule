from django import forms
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from schedule_tests.models import Club

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ('name', 'description')
