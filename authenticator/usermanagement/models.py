from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class BaseModel(models.Model):
    """
    Base model
    Attributes:
        created_at (datetime): Date and time of create
        updated_at (datetime): Date and time of update
        is_delete (bool): is the record is deleted
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(default=None,null=True)


    class Meta:
        """
        The Meta class allows customization and configuration of various aspects of the model.
        It is used to define metadata and specify additional options that control the behavior
        of the model in Django.
        """
        abstract = True

    def update(self, **kwargs):
        """
        The update method allows updating multiple instances of the model in the database
        in a single query, providing a more efficient way to perform bulk updates.
        """
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()

    def inactivate(self):
        """
        inactivate
        """
        self.deleted_at = datetime.now()
        self.save()

    def activate(self):
        """
        activate
        """
        self.deleted_at= None
        self.save()


class Roles(BaseModel):
    """
    User Roles
    """
    name = models.CharField(max_length=25)

class CustomUserManager(BaseUserManager):
    """
    CustomUserManager
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create User
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create Superuser
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    """
    Custom user model
    """
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)
