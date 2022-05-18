 
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from accounts.models import UserProfile  
from application.forms import *
from django.template import loader 
from django.contrib.auth.mixins import LoginRequiredMixin

from notifications.utilities import create_notification
# Create your views here.

class EmployerJobApplicationView(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    form_class = EmployerJobApplicationForm
    template_name = 'accounts/main/employers/application/index.html'
    
    def get(self,request): 
        profile = UserProfile.objects.get(user_id=request.user.id)  
        context = {
            "title":"Employer Applications",
            'form':self.form_class, 
            'profile':profile
        }
        return render(request, self.template_name,context)
   
    def post(self,request): 
        profile = UserProfile.objects.get(user_id=request.user.id)  
        form = self.form_class(request.POST)
        if form.is_valid(): 
            form.instance.user=profile
            form.instance.status=1 
            form.save()
            content = f"An application has been received from {request.user.email}"
            create_notification(request=request, notification_type=2, content=content)
            message = "success"
            return JsonResponse({"message":message})
        else:
            message = form.errors
            return JsonResponse({"message":message})  

class EmployerJobApplicationTableView(LoginRequiredMixin,View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request,  *args, **kwargs):
        template = loader.get_template("accounts/main/employers/application/table.html") 
        employer_job_applications = EmployerApplication.objects.all()
        context = { 
            'employers_job_applications': employer_job_applications
        }
        return HttpResponse(template.render(context, self.request))

class DeleteEmployerJobApplication(LoginRequiredMixin, View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
 
    def get(self, request, id, *args, **kwargs): 
        EmployerApplication.objects.get(id=id).delete()
        message = "success"
        return JsonResponse({"message": message })

