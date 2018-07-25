from django.db import models
from django.contrib.auth.models import  (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, userId, first_name, last_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email.")
        if not password:
            raise ValueError("Users must have a password.")
        if not userId:
            raise ValueError("Users must have a userId.")
        if not first_name or not last_name:
            raise ValueError("Users must have a name.")
        user_obj = self.model(
            email = self.normalize_email(email),
            userId = userId,
            first_name = first_name,
            last_name = last_name,
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, userId, first_name, last_name, password=None):
        user = self.create_user(
            email,
            userId,
            first_name,
            last_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, userId, first_name, last_name, password=None):
        user = self.create_user(
            email,
            userId,
            first_name,
            last_name,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    userId = models.CharField(primary_key=True, max_length=255)
    first_name = models.CharField(max_length=255,  default="your")
    last_name = models.CharField(max_length=255, default="name")
    is_active = models.BooleanField(default=True) #can login
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD =  'userId' #username
    # email and password are require by default
    REQUIRED_FIELDS = ['email','first_name','last_name']
    def __str__(self):
        try:
            return self.userId
        except Exception as e:
            return self.email

    def get_full_name(self):
        if self.first_name or self.last_name:
            full_name = self.first_name + ' ' + self.last_name
            return full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def staff(self):
        return self.is_staff

    @property
    def admin(self):
        return self.is_admin

    @property
    def active(self):
        return self.is_active


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # extend extra data

'''class extraauth(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    year = models.IntegerField(default=1)
    userId = models.CharField(default="",max_length=255)


class Tracker(models.Model):
    quizDone = models.IntegerField(default=0)
    quizTrack = models.FloatField(default=0)
    totalScore = models.FloatField(default=0)
    '''




