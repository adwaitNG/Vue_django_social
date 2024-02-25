import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **additional_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **additional_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **additional_fields):
        additional_fields.setdefault('is_staff', False)
        additional_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **additional_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **additional_fields):
        additional_fields.setdefault('is_staff', False)
        additional_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **additional_fields)
    
class User (AbstractBaseUser,PermissionsMixin):
    id =  models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
    email = models.EmailField( unique =True)
    name = models.CharField(max_length=255, blank=True, default='')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default =timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD =    'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []