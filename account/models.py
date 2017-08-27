from __future__ import unicode_literals

from django.contrib.auth.models import (PermissionsMixin, Group as BaseGroup, BaseUserManager, AbstractBaseUser)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email address must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    created_at = models.DateTimeField(_('time of creation'), null=True, auto_now_add=True)
    updated_at = models.DateTimeField(_('last modification time'), null=True, auto_now=True)
    email = models.EmailField(
        _('email address'),
        null=True,
        blank=True,
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },)
    first_name = models.CharField(_('first name'), max_length=32, blank=False)
    last_name = models.CharField(_('last name'), max_length=32, blank=False)
    address = models.CharField(_('address'), max_length=128, blank=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):

        return self.get_full_name()

    def __unicode__(self):
        
        return self.get_full_name()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return full_name = '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Group(BaseGroup):

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        proxy = True