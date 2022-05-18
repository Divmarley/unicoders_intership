from django.shortcuts import render
from django.views import View
from django.template import loader
from django.http import HttpResponse, JsonResponse
from accounts.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin 
from application.models import EmployerApplication, JobApplication
from notifications.models import Notification
from notifications.utilities import create_notification

# Create your views here.


class AdminListStudentJobApplicationView(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to" 
    template_name = 'accounts/main/staff/application/students/index.html'
    
    def get(self,request):
        profile = UserProfile.objects.get(user_id=request.user.id)
        notifications = Notification.objects.filter(notification_type=2, is_read=False)
        context = {
            "title":"Student Applications",
            "profile":profile,
            "notifications":notifications
            }
        return render(request, self.template_name, context) 
         
class AdminListStudentJobApplicationTableView(LoginRequiredMixin,View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request,  *args, **kwargs):
        template = loader.get_template("accounts/main/staff/application/students/table.html") 
        
        profile = UserProfile.objects.get(user_id=request.user.id) 
        student_job_applications = JobApplication.objects.all()
        notifications = Notification.objects.filter(notification_type=2, is_read=False)
        context = { 
            "notifications":notifications,
            'applications': student_job_applications,
            "profile":profile , 
        }
        return HttpResponse(template.render(context, self.request))

class AdminChangeStudentApplicationStatus(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    def get(self, request, id):
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if is_ajax:
            application = EmployerApplication.objects.get(id=id)
            if application.status == 4:
                application.status = 3
                content = "Your application has been successfully completed."
                create_notification(request, application.user.id, 2, content)
                return JsonResponse({"message":"Application status changed to Completed"})
            else:
                application.status = 4
                content = "Your application has been approved. Awaiting placement"
                create_notification(request, application.user.id, 2, content)
                return JsonResponse({"message":"Application status changed to Awaiting placement"})
        else:
            return JsonResponse({"message":"Something went wrong"})



class EmployerJobApplicationStaffView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request,  *args, **kwargs):
        template = loader.get_template("accounts/main/staff/application/employers/index.html")
        profile = UserProfile.objects.get(user_id=request.user.id) 
        # employer_job_applications = EmployerApplication.objects.all()
        notifications = Notification.objects.filter(notification_type=2, is_read=False)
        context = { 
            "notifications":notifications,
            'title': "Employer Applications",
            'profile':profile,
            # 'employee_applications': employer_job_applications
        }
        return HttpResponse(template.render(context, self.request))

class EmployerJobApplicationStaffTableView(LoginRequiredMixin,View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request,  *args, **kwargs):
        template = loader.get_template("accounts/main/staff/application/employers/table.html") 
        employer_job_applications = EmployerApplication.objects.filter(user=request.user.id)
        profile = UserProfile.objects.get(user_id=request.user.id) 
        context = { 
            'employer_job_applications': employer_job_applications,
            "profile":profile ,
        }
        return HttpResponse(template.render(context, self.request))

class AdminChangeEmployerApplicationStatus(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    def get(self, request, id):
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if is_ajax:
            application = EmployerApplication.objects.get(id=id)
            if application.status == 4:
                application.status = 3
                content = "Your application has been successfully completed."
                create_notification(request, application.user.id, 2, content)
                return JsonResponse({"message":"Application status changed to Completed"})
            else:
                application.status = 4
                content = "Your application has been approved. Awaiting placement"
                create_notification(request, application.user.id, 2, content)
                return JsonResponse({"message":"Application status changed to Awaiting placement"})
        else:
            return JsonResponse({"message":"Something went wrong"})

