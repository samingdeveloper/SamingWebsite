from django.db import models
from django.contrib.auth.models import  (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email.")
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password.")
        user_obj = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255,  blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True) #can login
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD =  'email' #username
    # email and password are require by default
    REQUIRED_FIELDS = ['username',]
    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name or self.last_name:
            full_name = self.first_name + self.last_name
            return full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # extend extra data

'''class extraauth(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    year = models.IntegerField(default=1)
    studentId = models.CharField(default="",max_length=255)


class Tracker(models.Model):
    quizDone = models.IntegerField(default=0)
    quizTrack = models.FloatField(default=0)
    totalScore = models.FloatField(default=0)
    '''




