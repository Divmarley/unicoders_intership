from audioop import reverse
import os
from django.dispatch import receiver 
from django.http import HttpRequest, HttpResponse, JsonResponse
from tempfile import template
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from application.models import JobApplication,EmployerApplication
from community.models import Community
from notifications.utilities import create_notification
from .models import Branch, SocialMediaLink, UserImage, UserProfile,Message
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME, update_session_auth_hash
from django.contrib import messages
from accounts.forms import CreateAccountForm, CreateProfileForm, CreateSocialMediaLinkViewForm, EditUserImageForm, LoginForm, MessageForm
from django.core.mail import send_mail, EmailMessage,EmailMultiAlternatives
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# landing page
class IndexView(View):
    def get(self,request):
        template_name='landing_page/index.html'
        context={
        }
        return render(request,template_name,context)
# Create Account
class CreateAccountView(View): 
    template_name='accounts/auth/signup.html'
    def get(self, request):
        form = CreateAccountForm
        if request.user.is_authenticated and request.user.is_active:
            return redirect("account:dashboard")
        else: 
            context={
                "form":form
            }
            return render(request,self.template_name,context)

    def post(self, request):
        form = CreateAccountForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email'] 
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save() 
            # subject, from_email, to = 'Welcome to Openlabs Ghana', 'uncoders@gmail.com', user.email
            # text_content = 'This is an important message.'
            # html_content = '<h1>thanks for joining our world unicoders says hello</h1>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            user = authenticate(email=email, password=password) 

            if user.is_active:
                if user.is_admin or user.is_superuser:
                    messages.error(request, 'You are not authourized.')
                else: 
                    login(request, user) 
                    try:
                        profile = UserProfile.objects.get(user_id=request.user.id)  
                        return redirect("account:dashboard")
                    except UserProfile.DoesNotExist:
                        return redirect("account:profile_create")
                        
            messages.error(request, 'You are not authourized.')
        return render(request, self.template_name, {'form': form.errors })
# login
class LoginView(View):
    form_class = LoginForm
    template_name = "accounts/auth/login.html"

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated and request.user.is_active :
            return redirect("account:dashboard")
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password) 
            if user.is_active:
                login(request, user)
                try:
                    profile = UserProfile.objects.get(user_id=request.user.id)  
                    return redirect("account:dashboard") 
                except UserProfile.DoesNotExist:
                    return redirect("account:profile_create")
            else:
                messages.error(request, 'Your account is not activated.')
        print(form.errors)
        return render(request, self.template_name, {'form': form })
# logout 
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')
# Dashboard
class DashboardView(LoginRequiredMixin,View): 
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    template_name='accounts/main/dashboard.html' 
    def get(self, request): 
        if request.user.is_authenticated and request.user.is_active :
           
            try:
                profile = UserProfile.objects.get(user_id=request.user.id)   
            except UserProfile.DoesNotExist:
                redirect_url = self.request.GET.get('redirect_to', 'account:profile_create')
                return redirect(redirect_url) 
            users =  UserProfile.objects.all().count()
            student_application =  JobApplication.objects.all().count()
            employer_application =  EmployerApplication.objects.all().count()
            community =  Community.objects.all().count()
            top_community = Community.objects.filter().order_by('?')[0:4]
            context={ 
                'title':"Dashboard",
                'profile':profile,
                "users":users,
                "student_application":student_application,
                "employer_application":employer_application,
                "community":community,
                "top_community":top_community
            
            }
            return render(request,self.template_name,context)
        else: 
            redirect_url = self.request.GET.get('redirect_to', 'account:login')
            return redirect(redirect_url)

class CreateProfileView(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    template_name='accounts/main/profile/create.html'

    def get(self, request): 
        branches = Branch.objects.all()
        context={ 
            "title":"Create Profile",
            "branch":branches
        }
        return render(request,self.template_name,context)

    def post(self,request):
        profile_form = CreateProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            profile =profile_form.save(commit=False) 
            profile.user_id = request.user.id
            profile.save() 
            
            return redirect("account:dashboard") 
        print(profile_form.errors)
        return render(request, self.template_name, {'form': profile_form})
 
class ProfileView(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    template_name='accounts/main/profile/index.html'
    def get(self, request): 
        social_media_link = SocialMediaLink.objects.filter(user_id=request.user.id) 
        profile = UserProfile.objects.get(user_id=request.user.id)  
        context={ 
            'profile':profile,
            "title":"Profile",
            'social_media_link':social_media_link
        }
        return render(request,self.template_name,context)

# class DetailProfileView(LoginRequiredMixin,View):
#     login_url = "account:login"
#     redirect_field_name = "redirect_to"
#     template_name='accounts/main/profile/detail.html'
#     def get(self, request, id): 
#         social_media_link = SocialMediaLink.objects.filter(user_id=request.user.id) 
#         profile = UserProfile.objects.get(user_id=id)  
#         context={ 
#             'profile':profile,
#             "title":"Profile",
#             'social_media_link':social_media_link
#         }
#         return render(request,self.template_name,context)


    # def get(self ,request , id):   
    #     # social_media_link = SocialMediaLink.objects.filter(user_id=id) 
        
    #     profile = UserProfile.objects.get(user_id=id)  
    #     context={ 
    #         'profile':profile,
    #         "title":"Profile",
    #         # 'social_media_link':social_media_link
    #     }
    #     return render(request,self.template_name,context)


class ProfleUpdateView(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
 
    def post(self,request):
        pass

class CreateProfileImgae(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    form_class = EditUserImageForm
    def post(self, request, id, *args, **kwargs):
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if is_ajax:
            profile = UserProfile.objects.get(id=id)
            data = {"image": profile.image}
            form = self.form_class(request.POST, request.FILES, initial=data)
            if form.is_valid():
                # check if image field is not empty
                if profile.image:
                    # check if image field path exist in directory
                    if os.path.exists(profile.image.path):
                        # remove from path and reupdate with the new one
                        os.remove(profile.image.path)
                        profile.image = request.FILES['image']
                        profile.save()
                        return JsonResponse({"message":"success", "img": profile.image.url})
                    else:
                        # update new image if theres no image in directory
                        profile.image = request.FILES['image']
                        profile.save()
                        return JsonResponse({"message":"success", "img": profile.image.url})
                else:
                    # update new image if there no image in the image field
                    profile.image = request.FILES['image']
                    profile.save()
                    # log_activity(self.request.user, self.request.user.business_id, "deactivated branch '"+branch.name+"'")
                    return JsonResponse({"message":"success", "img": profile.image.url})

            return JsonResponse({"message":"Validating image failed"})

class ResetPasswordView(View):
    template_name = "accounts/auth/forgot.html"

    def get(self, request): 
        return render(request, self.template_name, {})

    

# class ResetPasswordView(View):
#     template_name = "accounts/auth/forgot.html"

#     def get(self, request):
#         user = get_object_or_404(User, id=id)
#         user.set_password('123456')
#         user.save()
#         url = request.build_absolute_uri(reverse('account:login'))
#         send_mail(
#             'Password Reset',
#             f"Your password has been reset for you with new password: 123456. Use this link {url} to login.",
#             settings.DEFAULT_FROM_EMAIL,
#             [user.email],
#             fail_silently=False,
#         )
#         return render(request, self.template_name, {})

# class ChangePasswordView(View):
#     login_url = "accounts:login"
#     redirect_field_name = "redirect_to" 
#     template_name = "users/accounts/change_password.html"

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {})

#     def post(self, request, *args, **kwargs):
#         if request.is_ajax():
#             form = PasswordChangeForm(request.user, request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 update_session_auth_hash(request, user)  # Important! 
#                 return JsonResponse({"message": "success"})
#             else:
#                 return JsonResponse({"message": form.errors})
#         return HttpResponse('Wrong request')

# class ResetPasswordView( View):

#     def get(self, request, id, *args, **kwargs):
#         # if request.is_ajax():
#         user = get_object_or_404(User, pk=id)
#         user.set_password('123456')
#         user.save()
#         url = request.build_absolute_uri(reverse('account:login'))
#         send_mail(
#             'Password Reset',
#             f"Your password has been reset for you with new password: 123456. Use this link {url} to login.",
#             settings.DEFAULT_FROM_EMAIL,
#             [user.email],
#             fail_silently=False,
#         )
#         return JsonResponse({'message':'success'})
            
#         # return HttpResponse('Wrong request')

 
# class ChangePasswordView( View): 
#     template_name = 'accounts/auth/password/change.html'
    
#     # @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         if request.is_ajax():
#             form = PasswordChangeForm(request.user, request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 update_session_auth_hash(request, user)  # Important!
#                 log_activity(self.request.user, self.request.user.business_id, "Changed your password")
#                 return JsonResponse({"message": "success"})
#             else:
#                 return JsonResponse({"message": form.errors})



class CreateSocialMediaLinkView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to" 
    form_class = CreateSocialMediaLinkViewForm
    

    # def is_ajax(request):
    #     return request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if is_ajax:
            form = self.form_class(request.POST)
            if form.is_valid():
                profile_save =form.save(commit=False)
                form.instance.user_id = request.user
                profile_save.save()
                return JsonResponse({'message':'success'})
            return JsonResponse({'message':form.errors})
        return HttpResponse('Wrong request')

    # def post(self, *args, **kwargs):
    #     if self.request.is_ajax and self.request.method == "POST":
    #         form = self.form_class(self.request.POST)
    #         if form.is_valid():
    #             instance = form.save()
    #             # ser_instance = serializers.serialize('json', [ instance, ])
    #             # send to client side.
    #             return JsonResponse({"instance": 'ser_instance'}, status=200)
    #         else:
    #             return JsonResponse({"error": form.errors}, status=400)

    #     return JsonResponse({"error": ""}, status=400)


# class SendMessage(View):
#     def post(self,request, id):
#         error = "Unable to send message"
#         is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
#         if is_ajax:
#             user=get_object_or_404(pk=id)
#             content = request.POST.get('content')
#             create_notification(request, user.id, 1, content)
#             return JsonResponse({'message':'success'})
#         return JsonResponse({'message':error})

class UserMessage(View):
    form = MessageForm()

    def get(self,request):
        template = "message/messages.html"
        msg = Message.objects.all()
        received_messages = Message.objects.filter(receiver=request.user)
        sent_messages = Message.objects.filter(sender=request.user)
        context = {
            "form":self.form,
            "received_messages": received_messages,
            "sent_messages":sent_messages,
            "msg":msg
        }
        return render(request, template, context)

    def post(self, request):
        context={"msg":"Success"}
        if self.form.is_valid():
            self.form.instance.sender=request.user
            # receiver = self.form.cleaned_data('receiver')
            # message = self.form.cleaned_data('message')
            self.form.save()
        return HttpResponse("yes")
            