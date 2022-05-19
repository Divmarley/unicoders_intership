 
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from accounts.models import UserProfile 
from notifications.utilities import create_notification 
from django.template import loader
from application.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class JobListView(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    # form_class = AdminJobApplicationForm
    template_name = 'accounts/main/jobs/index.html'
    
    def get(self,request):
        profile = UserProfile.objects.get(user_id=request.user.id)    
        context = {
            "title":"Jobs",
            "profile":profile , 
            }
        return render(request, self.template_name, context)
    