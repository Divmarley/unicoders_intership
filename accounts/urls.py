from django.urls import path, reverse_lazy 
from accounts.views import * 
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name='account'
urlpatterns = [ 
    path('', IndexView.as_view(),name ='index'),
    path('signup', CreateAccountView.as_view(),name ='signup'),
    path('login', LoginView.as_view(),name ='login'),
    path('dashboard', DashboardView.as_view(),name ='dashboard'),
    path('logout', LogoutView.as_view(),name ='logout'),
    path('profile', ProfileView.as_view(),name ='profile'), 
    path('create-profile', CreateProfileView.as_view(),name ='profile_create'),
    path('profile-edit/<int:id>', ProfleUpdateView.as_view(),name ='profile-edit'),
    path('profile/change-password', ChangePasswordView.as_view(), name="change-password"),
    path('create-social-link', CreateSocialMediaLinkView.as_view(), name='create-social-link'),
    path('create-skill', CreateSkillView.as_view(), name='create-skill'),
    path('profile/<int:id>/change-profile-image', CreateProfileImgae.as_view(), name="change-profile-image"),
    path('message/', UserMessage.as_view(), name="messages"),


    path('password-reset/', PasswordResetView.as_view(
        email_template_name= 'auth/password/password_reset_email.html',
        html_email_template_name= 'auth/password/password_reset_email.html',
        success_url = reverse_lazy('accounts:password_reset_done'), 
        subject_template_name = 'auth/password/password_reset_subject.txt',
        template_name = 'accounts/auth/forgot.html'
        ), name='password_reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name = 'auth/password/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        success_url = reverse_lazy('accounts:password_reset_complete'),
        template_name = 'auth/password/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name = 'auth/password/password_reset_complete.html'
    ), name='password_reset_complete'), 


    path('password-set/<uidb64>/<token>/', SetUserPasswordView.as_view(), name='password_set'),
]

 