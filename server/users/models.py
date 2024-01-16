from django.db.models import CharField, DateTimeField, BooleanField, EmailField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(email=self.normalize_email(
            email), )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=self.normalize_email(
            email), password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    email = EmailField(max_length=100, unique=True, db_collation='case_insensitive')
    first_name = CharField(max_length=100, null=True, blank=True)
    last_name = CharField(max_length=100, null=True, blank=True)
    date_joined = DateTimeField(auto_now_add=True)
    last_login = DateTimeField(auto_now=True)
    is_admin = BooleanField(default=False)
    is_active = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
   
    USERNAME_FIELD = 'email'
    
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # for permissions, to keep it simple, all admins have all permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # does this user has permission to view app, always yes for simplicity
    def has_module_perms(self, app_label):
        return True