from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth import settings

# Create your models here.


class Designation(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Designations"
        verbose_name = "Designation"

    def __str__(self):
        return self.name


class Employee(models.Model):
    objects = models.Manager

    class gender(models.IntegerChoices):
        MALE = 1
        FEMALE = 2
        OTHER = 3

    class marital_status(models.IntegerChoices):
        MARRIED = 1
        UNMARRIED = 2

    class job_Type(models.IntegerChoices):
        FULL_TIME = 1
        HALF_TIME = 2

    class nationality(models.IntegerChoices):
        INDIAN = 1

    class experience(models.IntegerChoices):
        ONE_YEAR = 1
        TWO_YEAR = 2
        THREE_YEAR = 3
        FOUR_YEAR = 4
        FIVE_YEAR_OR_PLUS = 5

    name = models.CharField(max_length=150)
    email = models.EmailField(
        max_length=150, null=True, blank=True)
    password = models.CharField(max_length=150, null=True, blank=True)
    mobile_no = models.CharField(max_length=10, null=True, blank=True)
    gender = models.IntegerField(
        choices=gender.choices, default=gender.MALE)
    marital_status = models.IntegerField(
        choices=marital_status.choices, default=marital_status.MARRIED)
    job_Type = models.IntegerField(
        choices=job_Type.choices, default=job_Type.FULL_TIME)
    experience = models.IntegerField(
        choices=experience.choices, default=experience.ONE_YEAR)
    nationality = models.IntegerField(
        choices=nationality.choices, default=nationality.INDIAN)
    pan_no = models.CharField(max_length=150, null=True, blank=True)
    aadhar_no = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)

    address = models.TextField(null=True, blank=True)
    state = models.ForeignKey(
        'settings.state', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    district = models.ForeignKey(
        'settings.District', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    post_office = models.CharField(max_length=150, null=True, blank=True)
    police_station = models.CharField(max_length=150, null=True, blank=True)
    pin_code = models.CharField(max_length=150, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    designation = models.ForeignKey(
        Designation, on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    religion = models.ForeignKey(
        'students.Religion', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    qualification = models.ForeignKey(
        'students.Qualification', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to='employee/', max_length=150, null=True, blank=True,help_text = "Your image should be lower 500kb.")
    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Employees"
        verbose_name = "Employee"

    def __str__(self):
        return self.name


class EmpAttendance(models.Model):
    objects = models.Manager

    date = models.DateField(default=datetime.now)

    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True})

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Attendance"
        verbose_name = "Attendance"

    def __str__(self):
        return str(self.date)


class EmpAttendanceDetails(models.Model):
    objects = models.Manager

    class type(models.IntegerChoices):
        PRESENT = 0
        ABSENT = 1
        LEAVE = 2

    attendance = models.ForeignKey(
        EmpAttendance, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    is_present = models.IntegerField(
        choices=type.choices, default=type.PRESENT)
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Attendanc Details"
        verbose_name = "Attendance Details"

    def __str__(self):
        return self.employee.name
