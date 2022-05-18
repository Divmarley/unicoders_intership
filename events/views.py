from asyncio import events
import json
from multiprocessing import context
import re
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from json import dumps
from django.views import View

from accounts.models import UserProfile

from.forms import CreateEventForm
from.models import Event

# Create your views here.
class EventView(View):
    form_class=CreateEventForm
    template_name='accounts/main/events/index.html'
    def get(self, request):
        event = Event.objects.all() 
        mpJson = serializers.serialize("jsonl",event) 
        # print(type(list(mpJson)))
        profile = UserProfile.objects.get(user_id=request.user.id) 
        context={ 
            'profile':profile,
            'data':mpJson
        }
        return render(request,self.template_name,context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            event =form.save(commit=False) 
            event.save()
            return JsonResponse({'message':'success'})
        print(form.errors)
        return render(request, self.template_name, {})


class EventDetailView(View):
    def get(self,request, *args,slug, **kwargs):
        template_name="accounts/main/events/detail.html" 
        event = Event.objects.get(slug=slug)
        context={'event':event}
        return render(request,template_name,context)