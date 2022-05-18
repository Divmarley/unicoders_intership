from django.urls import path

from events.views import EventView ,EventDetailView
app_name='event'
urlpatterns = [ 
    path('',EventView.as_view(),name="index"),
    path('<str:slug>/',EventDetailView.as_view(),name="detail")
 
]
