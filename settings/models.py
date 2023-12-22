from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth import settings

# Create your models here.


class State(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)
   
    class Meta:
        verbose_name_plural = "States"
        verbose_name = "State"

    def __str__(self):
        return self.name


class District(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, limit_choices_to={'is_active': True})

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)
    
    class Meta:
        verbose_name_plural = "Districts"
        verbose_name = "District"

    def __str__(self):
        return self.name


class Tinify(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150)
    api_key = models.CharField(max_length=150, unique=True)
    count = models.IntegerField(default=0)
    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)
    
    class Meta:
        verbose_name_plural = "Tinify API"
        verbose_name = "Tinify"

    def __str__(self):
        return self.name

class Plan(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)
    details = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    
    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)
 
    class Meta:
        verbose_name_plural = "Plans"
        verbose_name = "Plan"

    def __str__(self):
        return self.name

class Role(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150)
    
    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)
 
    class Meta:
        verbose_name_plural = "Roles"
        verbose_name = "Role"

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Payment Method"
        verbose_name = "Payment Method"

    def __str__(self):
        return self.name
