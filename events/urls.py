# from django.urls import path

# from events.views import EventView ,EventDetailView
# app_name='event'
# urlpatterns = [ 
#     path('',EventView.as_view(),name="index"),
#     path('<str:slug>/',EventDetailView.as_view(),name="detail")
 
# ]

from django.urls import path
from .views import *
app_name = "event"
urlpatterns = [
    path("calender/", CalendarViewNew.as_view(), name="calendar"),
    path("calenders/", CalendarView.as_view(), name="calendars"),
    path("event/new/", create_event, name="event_new"),
    path("event/edit/<int:pk>/", EventEdit.as_view(), name="event_edit"),
    path("event/delete/<int:id>/", DeleteEvent.as_view(), name="event_delete"),
    path("event/<int:event_id>/details/", event_details, name="event-detail"),
    path(
        "add_eventmember/<int:event_id>", add_eventmember, name="add_eventmember"
    ),
    path(
        "event/<int:pk>/remove",
        EventMemberDeleteView.as_view(),
        name="remove_event",
    ),
    path("all-event-list/", AllEventsListView.as_view(), name="all_events"),
    path(
        "running-event-list/",
        RunningEventsListView.as_view(),
        name="running_events",
    ),
]
