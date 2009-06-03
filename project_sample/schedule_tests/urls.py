from django.conf.urls.defaults import *
 
urlpatterns = patterns('',    
    url(r'^$', 'schedule_tests.views.list_clubs', name="list_clubs"),
    # clubs
    url(r'^club/create$', 
        'schedule_tests.views.create_club', name="create_club"),
    url(r'^club/show/(?P<club_id>\d+)$', 'schedule_tests.views.show_club', 
        name="show_club"),
    url(r'^club/timeline/(?P<club_id>\d+)$', 'schedule_tests.views.show_club_timeline', 
        name="show_club_timeline"),
    url(r'^club/edit/(?P<club_id>\d+)$', 'schedule_tests.views.edit_club', 
        name="edit_club"),
    url(r'^club/delete/(?P<club_id>\d+)$', 'schedule_tests.views.delete_club', 
        name="delete_club"),
    # meetings
    url(r'^meetings$', 'schedule_tests.views.list_meetings', name="list_meetings"),

    url(r'^meetings/calendar$', 'schedule_tests.views.list_meetings_calendar', name="list_meetings_calendar"),
    url(r'^meetings/timeline$', 'schedule_tests.views.list_meetings_timeline', name="list_meetings_timeline"),
    url(r'^meetings/timeline_data$', 'schedule_tests.views.meetings_timeline_data', name="meetings_timeline_data"),
    
    url(r'^meeting/create/(?P<club_id>\d+)$',
        'schedule_tests.views.create_meeting', name="create_meeting"),
    url(r'^meeting/show/(?P<meeting_id>\d+)$', 'schedule_tests.views.show_meeting', 
        name="show_meeting"),
    url(r'^meeting/edit/(?P<meeting_id>\d+)$', 'schedule_tests.views.edit_meeting', 
        name="edit_meeting"),
    url(r'^meeting/delete/(?P<meeting_id>\d+)$', 'schedule_tests.views.delete_meeting', 
        name="delete_meeting"),
)

