from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            user_name=user_name,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    user_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Blog(models.Model):
    blog_title=models.CharField(max_length=1000)
    blog_date=models.DateField()
    blog_question=models.CharField(max_length=100)
    blog_description=models.TextField(max_length=100)
    blog_image=models.ImageField(default="", upload_to='blog/images')
    is_admin = models.BooleanField(default=True)

    def __str__(self):
        return self.blog_title

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



class BooksAndBrochure(models.Model):
    SELECT_TYPE_CHOICES = [
        ('BOOK', 'Books'),
        ('BRO', 'Brochure')
    ]
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    publisher=models.CharField(max_length=100)
    description=models.TextField(max_length=100)
    type=models.CharField(choices=SELECT_TYPE_CHOICES,max_length=10)
    category=models.CharField(max_length=100)
    image=models.ImageField(upload_to='books/image')
    book = models.FileField(upload_to='books/pdf',default="")
    YOP=models.PositiveIntegerField()
    pages=models.PositiveIntegerField()
    view=models.PositiveIntegerField()
    read=models.PositiveIntegerField()


    