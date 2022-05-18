from dataclasses import field
from django import forms
from django.contrib.auth import authenticate
from accounts.models import Message, SocialMediaLink, User, UserImage, UserProfile

class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','account_type', 'password']
 
class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password') 

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login credentials.")

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','location','bio','gender','phone','address','image','branch']

class EditUserImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']     

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','location','bio','gender','phone','address']

class SetPasswordForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)

    # def clean(self):
    #     if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
    #         if self.cleaned_data['password1'] != self.cleaned_data['password2']:
    #             raise forms.ValidationError(_("The two password fields did not match."))
    #     return self.cleaned_data 

    class Meta:
        model = User
        fields = ["password"]
 
class CreateSocialMediaLinkViewForm(forms.ModelForm):
    class Meta:
        model = SocialMediaLink
        fields = ['social_media_field','link'] 

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields=['receiver', 'message']