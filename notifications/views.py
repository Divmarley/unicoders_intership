from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.models import Notification

# Create your views here.
class ChangeNotificationStatusView(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to" 
 
    def get(self,request,id): 
        noti = Notification.objects.get(id=id)
        if noti.is_read:
            noti.is_read = False
            noti.save()
            message = "success"
            return JsonResponse({"message":message})
        else: 
            noti.is_read=True
            message = "success"
            noti.save()
            return JsonResponse({"message":message})
            noti.save()
         
