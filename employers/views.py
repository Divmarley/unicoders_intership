 
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from accounts.models import UserProfile  
from application.forms import *
from django.template import loader 
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.models import Notification

from notifications.utilities import create_notification
# Create your views here.

class EmployerJobApplicationView(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    form_class = EmployerJobApplicationForm
    template_name = 'accounts/main/employers/application/index.html'
    
    def get(self,request): 
        profile = UserProfile.objects.get(user_id=request.user.id)
        notifications = Notification.objects.filter(notification_type=1, is_read=False, to_user=request.user)

        context = {
            'notifications': notifications,
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


class ChangeEmployerApplicationStatus(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    def get(self, request, id):
        application = EmployerApplication.objects.get(id=id)
        profile = None
        try:
            profile = UserProfile.objects.get(id=application.user.id)
            if application.status == 1:
                application.status = 2
                application.save()
                content = "Your application is awaiting placement."
                create_notification(request, profile.user, 1, content)
                return redirect(reverse_lazy("staff:employer-jp-index"))
                # return JsonResponse({"message":"Application status changed to Completed"})
            elif application.status == 2:
                application.status = 3
                application.save()
                content = "Your application has been approved."
                create_notification(request, profile.user, 1, content)
                return redirect(reverse_lazy("staff:employer-jp-index"))
                # return JsonResponse({"message":"You have been placed sucessfully"})
            elif application.status == 3:
                application.status = 3
                application.save()
                return redirect(reverse_lazy("staff:employer-jp-index"))

        except UserProfile.DoesNotExist: pass