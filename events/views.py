# from asyncio import events
# import json
# from multiprocessing import context
# import re
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.core import serializers
# from json import dumps
# from django.views import View

# from accounts.models import UserProfile

# from.forms import CreateEventForm
# from.models import Event

# # Create your views here.
# class EventView(View):
#     form_class=CreateEventForm
#     template_name='accounts/main/events/index.html'
#     def get(self, request):
#         event = Event.objects.all() 
#         mpJson = serializers.serialize("jsonl",event) 
#         # print(type(list(mpJson)))
#         profile = UserProfile.objects.get(user_id=request.user.id) 
#         context={ 
#             'profile':profile,
#             'data':mpJson
#         }
#         return render(request,self.template_name,context)

#     def post(self, request):
#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             event =form.save(commit=False) 
#             event.save()
#             return JsonResponse({'message':'success'})
#         print(form.errors)
#         return render(request, self.template_name, {})


# class EventDetailView(View):
#     def get(self,request, *args,slug, **kwargs):
#         template_name="accounts/main/events/detail.html" 
#         event = Event.objects.get(slug=slug)
#         context={'event':event}
#         return render(request,template_name,context)

from django.views.generic import ListView
# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from accounts.models import UserProfile
from events.models import EventMember, Event
from events.utils import Calendar
from events.forms import EventForm, AddMemberForm
from django.http import JsonResponse
from django.views.generic import View

from notifications.models import Notification



def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "accounts:signin"
    model = Event
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


@login_required(login_url="signup")
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("event:calendar"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"


@login_required(login_url="signup")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data["user"]
                EventMember.objects.create(event=event, user=user)
                return redirect("event:calendar")
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("event:calendar")


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "accounts/main/events/index.html"
    form_class = EventForm

    def get(self, request):
        forms = self.form_class()
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        notifications = []
        try:
            profile = UserProfile.objects.get(user_id=request.user.id)   
        except UserProfile.DoesNotExist:
            redirect_url = self.request.GET.get('redirect_to', 'account:profile_create')
            return redirect(redirect_url)
        if request.user.account_type == 1:
            notifications = Notification.objects.filter(notification_type=2, is_read=False)
        elif request.user.account_type == 2 or request.user.account_type == 3:
            notifications = Notification.objects.filter(notification_type=1, is_read=False, to_user=request.user)
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),

                }
            )
        context = {"form": forms, "events": event_list,
                   "events_month": events_month,"profile":profile,"notifications":notifications}
        return render(request, self.template_name, context)

    def post(self, request):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("event:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)




class AllEventsListView(ListView):
    """ All event list views """

    template_name = "event/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.all().order_by('start_time')


class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "event/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_running_events(user=self.request.user)

class DeleteEvent(LoginRequiredMixin, View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
 
    def get(self, request, id, *args, **kwargs): 
        Event.objects.get(id=id).delete()
        message = "success"
        return JsonResponse({"message": message })
