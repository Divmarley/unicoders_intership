from django.contrib import admin

from accounts.models import User,UserImage,SocialMediaLink,UserProfile,SocialMediaLink

# Register your models here.
admin.site.register(User)
admin.site.register(UserImage)
admin.site.register(SocialMediaLink)
admin.site.register(UserProfile) 