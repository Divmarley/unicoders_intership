from email import message
from urllib import request
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string


class MyUserManager(BaseUserManager):
    def create_user(self, email, account_type, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        # if not name:
        #     raise ValueError('Users must have name')
        # if not center:
        #     raise ValueError('Users must have center type')

        user = self.model(
            email=self.normalize_email(email),
            # name=name,
            account_type=account_type,
            # center=center,
            # fields=fields,
            # phone=phone 
        )

        user.is_active = True
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,account_type, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            # name=name,
            account_type=account_type,
            password=password,
            # center=center,
            # fields=fields,
            # phone=phone
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

user_type=  (
    ('super','super'),
    ('admin','admin'), 
    ('alumni','alumni'),
    ('company_owner','company owner'),
)
center_type=  (
    ('accra','Accra'),
    ('tema','Tema'), 
    ('takoradi','Takoradi'),
    ('tamale','Tamale'),
    ('kumasi','Kumasi'),
)
field_type=  (
    ('fullstack' , 'fullstack'),
    ('networking' , 'networking'),   
)

account_type=  (
    (1 , 'Staff'),
    (2 , 'Student'),   
    (3 , 'Organisation'),        
)

class User(AbstractBaseUser): 
    email = models.EmailField(max_length=255, unique=True) 
    account_type =models.IntegerField(choices=account_type) 
    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['account_type']

    objects = MyUserManager()

    class Meta:
        db_table = "user"
        

    def __str__(self):
        return f"{ self.email }"

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    @property
    def get_random_password(self):
        return get_random_string(length=6)

    @property
    def get_status(self):
        if self.is_active:
            return 'Deactivate'
        return 'Activate'

    @property
    def user_type(self):
        if self.account_type == 1:
            return 'Admin'
        elif self.account_type == 2:
            return 'Staff'
        elif self.account_type == 3:
            return 'Student'
        else:
            return 'Organisation'

class UserImage (models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_image", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="users", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "user_image"

    #Methods
    def __str__(self):
        return f"{self.user}"


    @property
    def get_user_image(self):
        if self.image:
            return self.image.url
        return 'assets/images/user.svg'

social_media_type= (
    ('facebook' , 'facebook'),
    ('linkedin' , 'linkedin'), 
    ('instagram' , 'instagram'), 
    ('twitter' , 'twitter'), 
    
    
)
class SocialMediaLink(models.Model):
    user_id = models.ForeignKey("accounts.User", verbose_name="users", on_delete=models.CASCADE)
    social_media_field =models.CharField(max_length=100,choices=social_media_type)  
    link  = models.CharField(max_length=255)

    class Meta :
        db_table = "social_media_link"
    
    def __str__(self):
        return f"{self.user_id }"

gender_type =  (
    ('m' , 'M'),
    ('f' , 'F'),   

)

class Branch(models.Model):
    name= models.CharField(max_length=255)
    slug = models.SlugField()
    class Meta :
        db_table = "branch"

class UserProfile(models.Model):
    user = models.ForeignKey('User', related_name='user', on_delete=models.CASCADE)
    branch = models.ForeignKey('Branch', related_name='branch', on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    address =  models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to="users", null=True)
    bio= models.TextField(null=True)
    gender =models.CharField(max_length=10,choices=gender_type) 
    phone = models.CharField(max_length=20)  
    
    class Meta :
        db_table = "profile"

    def __str__(self):
        return self.name

rating = (
    (10 , 10),
    (20 , 20), 
    (30 , 30), 
    (40 , 40), 
    (50 , 50), 
    (60 , 60), 
    (70 , 70), 
    (80 , 80), 
    (90, 90), 
    (100,100), 
    
    
)
class SkillSet (models.Model):
    user = models.ForeignKey('User', related_name='user_skill', on_delete=models.CASCADE)
    name = models.CharField(max_length=60, unique=True)
    rating = models.IntegerField(choices=rating)
 
    class Meta :
        db_table = "skill_set"

#     #Methods
    def __str__(self):
        return self.name

#     @property
#     def get_status(self):
#         if self.is_active:
#             return 'Deactivate'
#         return 'Activate'

class Message(models.Model):
    sender = models.ForeignKey('User', related_name='message_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey('User', related_name='message_receiver', on_delete=models.CASCADE)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"