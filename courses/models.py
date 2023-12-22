from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth import settings

# Create your models here.


class Duration(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150)
    total_month = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Franchise_point = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Durations"
        verbose_name = "Duration"

    def __str__(self):
        return self.name


class Course(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=150, unique=True)
    duration = models.ForeignKey(
        Duration, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    thubnail_image = models.ImageField(
        upload_to='course/', max_length=150)
    short_content = models.TextField()

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Courses"
        verbose_name = "Course"

    def __str__(self):
        return self.name


class AssignCourse(models.Model):
    objects = models.Manager

    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, limit_choices_to={'is_active': True}, default=1)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Default Column Name
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Assign Courses"
        verbose_name = "Assign Course"

    def __str__(self):
        return self.franchise.name
