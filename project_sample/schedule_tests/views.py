import uuid, datetime

import elementtree.ElementTree as ET

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from schedule.models import Calendar, CalendarRelation, Event, EventRelation
from schedule.filters import apply_date_filter
from schedule.views import create_event_node
from schedule_tests.models import Club, ClubMeeting
from schedule_tests.forms import ClubForm, MeetingForm

def create_club(request, template_name="schedule_tests/clubs/new.html"):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.save()
            calendar = Calendar(name = "%s Calendar" % club.name, slug = unicode(uuid.uuid1()))
            calendar.save()
            CalendarRelation.objects.create_relation(calendar, club, distinction="default", inheritable=True)
            
            return HttpResponseRedirect(reverse('show_club', args=(club.id,)))
        # if invalid, it gets displayed below
    else:
        form = ClubForm()
 
    return render_to_response(template_name, {'form': form,},
                              context_instance=RequestContext(request))

def edit_club(request, club_id,
    template_name="schedule_tests/clubs/edit.html"):
    club = get_object_or_404(Club, id = club_id)
 
    if request.method == 'POST':
        form = ClubForm(request.POST, instance = club)
        if form.is_valid():
            # create it
            club = form.save(commit=False)
            club.save()
            
            return HttpResponseRedirect(reverse('show_club', args=(club.id,)))
        # if invalid, it gets displayed below
    else:
        form = ClubForm(instance = club)
 
    return render_to_response(template_name, {
        'form': form,
        'club': club,
    }, context_instance=RequestContext(request))

def show_club(request, club_id,
    template_name="schedule_tests/clubs/details.html"):
    club = get_object_or_404(Club, id = club_id)
    return render_to_response(template_name, {
        'club': club,
    }, context_instance=RequestContext(request))

def show_club_timeline(request, club_id,
    template_name="schedule_tests/clubs/timeline.html"):
    club = get_object_or_404(Club, id = club_id)
    return render_to_response(template_name, {
        'club': club,
    }, context_instance=RequestContext(request))
    
def list_clubs(request, template_name = "schedule_tests/clubs/list.html"):
    clubs = Club.objects.order_by("name")
    
    return render_to_response(template_name, {
        'clubs': clubs,
    }, context_instance = RequestContext(request))

def delete_club(request, club_id):
    
    club = get_object_or_404(Club, id = club_id)
    club.delete()
    
    return HttpResponseRedirect(reverse('list_clubs'))    

def list_meetings(request, template_name = "schedule_tests/meetings/list.html"):
    meetings = ClubMeeting.objects.order_by("start")
    meetings = apply_date_filter(meetings, request)
    
    return render_to_response(template_name, {
        'meetings': meetings,
    }, context_instance = RequestContext(request))
    
def list_meetings_calendar(request, template_name = "schedule_tests/meetings/calendar.html"):
    return render_to_response(template_name, {
        'meetings': meetings,
    }, context_instance = RequestContext(request))
    
def list_meetings_timeline(request, template_name = "schedule_tests/meetings/timeline.html"):
    return render_to_response(template_name, {
    }, context_instance = RequestContext(request))
    
def meetings_timeline_data(request):
    meetings = ClubMeeting.objects.order_by("start")
    meetings = apply_date_filter(meetings, request)
    
    head = ET.Element('data')

    for meeting in meetings:
        for occurence in meeting.occurrences_after():
            create_event_node(head, occurence)

    return HttpResponse(ET.tostring(head), mimetype="text/xml")

def create_meeting(request, club_id,
                   template_name="schedule_tests/meetings/new.html"):

    club = get_object_or_404(Club, id = club_id)
 
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            calendar = Calendar.objects.get_calendar_for_object(club)
            
            meeting = form.save(commit=False)
            meeting.club = club
            meeting.calendar = calendar
            meeting.creator = request.user
            meeting.title = meeting.place
            meeting.save()
            
            return HttpResponseRedirect(reverse('show_meeting', args=(meeting.id,)))
        # if invalid, it gets displayed below
    else:
        form = MeetingForm(initial = {'club': club, 'start': datetime.datetime.now(), 'end': datetime.datetime.now()})
 
    return render_to_response(template_name, {
            'form': form,
            'club': club
        }, context_instance=RequestContext(request))

def edit_meeting(request, meeting_id,
    template_name="schedule_tests/meetings/edit.html"):
    meeting = get_object_or_404(ClubMeeting, id = meeting_id)
 
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance = meeting)
        if form.is_valid():
            event = EventRelation.objects.get_events_for_object(meeting, inherit=False)[0]
            event.start = form.cleaned_data['start']
            event.end = form.cleaned_data['end']
            event.title = form.cleaned_data['place']
            event.save()
            
            meeting = form.save(commit=False)
            meeting.save()
            
            return HttpResponseRedirect(reverse('show_meeting', args=(meeting.id,)))
        # if invalid, it gets displayed below
    else:
        form = MeetingForm(instance = meeting)
 
    return render_to_response(template_name, {
        'form': form,
        'meeting': meeting,
    }, context_instance=RequestContext(request))

def show_meeting(request, meeting_id,
    template_name="schedule_tests/meetings/details.html"):
    
    meeting = get_object_or_404(ClubMeeting, id = meeting_id)
    return render_to_response(template_name, {
        'meeting': meeting,
    }, context_instance=RequestContext(request))

def delete_meeting(request, meeting_id):
    
    meeting = get_object_or_404(ClubMeeting, id = meeting_id)
    club = meeting.club
    meeting.delete()
    
    return HttpResponseRedirect(reverse('show_club', args=(club.id,)))
