from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth import settings
from franchises.models import Franchise
# from exams.models import AdmitCard

# Create your models here.
def max_St_Code(franchise__id):
    obj_fr = Franchise.objects.get(pk=franchise__id)
    Is_code =  Student.objects.filter(franchise=obj_fr).count()
    
    if Is_code>0 :
        obj = Student.objects.filter(franchise=obj_fr).order_by('-id')[0]
        st_code = obj.code
        st_code = st_code[4:]
        st_code = int(st_code)
        st_code+=1
       
        var = 'UTEC'+str(st_code).zfill(10)
        return var
    else:
        
        code = obj_fr.code
        return code+'000101'

class Days(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Days"
        verbose_name = "Day"

    def __str__(self):
        return self.name


class Religion(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Religions"
        verbose_name = "Religion"

    def __str__(self):
        return self.name


class Category(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self):
        return self.name


class Qualification(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Qualifications"
        verbose_name = "Qualification"

    def __str__(self):
        return self.name


class RankType(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Rank Types"
        verbose_name = "RankType"

    def __str__(self):
        return self.name


class EnquirySource(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Enquiry Sources"
        verbose_name = "Enquiry Source"

    def __str__(self):
        return self.name


class Student(models.Model):
    objects = models.Manager

    class gender(models.IntegerChoices):
        MALE = 1
        FEMALE = 2
        OTHER = 3

    class marital_status(models.IntegerChoices):
        MARRIED = 1
        UNMARRIED = 2

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=150, unique=True,
                            editable=False, null=True, blank=True)
    email = models.EmailField(
        max_length=150, unique=True, null=True, blank=True)
    mobile_no = models.CharField(max_length=10)
    password = models.CharField(max_length=15, null=True, blank=True)
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)

    gender = models.IntegerField(
        choices=gender.choices, default=gender.MALE, null=True, blank=True)
    marital_status = models.IntegerField(
        choices=marital_status.choices, default=marital_status.MARRIED, null=True, blank=True)

    father_name = models.CharField(max_length=150)
    mother_name = models.CharField(max_length=150, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    religion = models.ForeignKey(
        Religion, on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    qualification = models.ForeignKey(
        Qualification, on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    address = models.TextField()
    state = models.ForeignKey(
        'settings.state', on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    district = models.ForeignKey(
        'settings.District', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    city = models.CharField(max_length=150)
    pin_code = models.CharField(max_length=150)
    
    profile_image = models.ImageField(upload_to='student/', max_length=150,
                    help_text = "Your image should be lower 500kb.")
    aadhar_card_image = models.ImageField(
        upload_to='student/', max_length=150)

    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True})

    enquiry_source = models.ForeignKey(
        EnquirySource, on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    source_code = models.CharField(verbose_name="Enrolment Number",max_length=150, null=True, blank=True)
    is_certified = models.BooleanField(default=False, null=True, blank=True)
    pass_out_date = models.DateField(null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    last_period_date = models.DateField(null=True, blank=True)
    is_drop_out = models.BooleanField(default=False, null=True, blank=True)
    form_code = models.CharField(max_length=150, null=True, blank=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    def is_admitcard(self):

        objcount = AdmitCard.objects.filter(student_id=self.id).count()

        if objcount>0:
            return True
        else:
            return False

    def is_admitcard_activated(self):

        obj = AdmitCard.objects.get(student_id=self.id)

        return obj.is_activated
        
    
    def is_admitcard_Code(self):

        obj = AdmitCard.objects.get(student_id=self.id)

        return obj.Code
        
    def gender_str(self):
        data = ['NA', 'Male', 'Female', 'Other']
        return data[int(self.gender)]
        
    def marital_status_str(self):
        data = ['NA', 'Married', 'Unmarried']
        return data[int(self.gender)]
    class Meta:
        verbose_name_plural = "Students"
        verbose_name = "Student"

    def __str__(self):
        return self.name

class Facilities(models.Model):
    objects = models.Manager

    
    
    name = models.CharField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    
    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Facilities"
        verbose_name = "Facilities"

    def __str__(self):
        return self.name

class Other_Facilities(models.Model):
    
    objects = models.Manager

    
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    facilities = models.ForeignKey(
        Facilities, on_delete=models.CASCADE, limit_choices_to={'is_active': True})

    
    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Other Facilities"
        verbose_name = "Other Facilities"

    def __str__(self):
        return self.student.name

class Timetable(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, default='')
    start_time = models.TimeField(default=datetime.now)
    end_time = models.TimeField(default=datetime.now)

    days = models.ManyToManyField(Days, limit_choices_to={
                                  'is_active': True})
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Timetables"
        verbose_name = "Timetable"

    def view_days(self):
        rslt = []
        rslt = [t.name for t in self.days.all()]
        return rslt

    def __str__(self):
        return str(self.start_time) + ' - '+str(self.end_time)


class TimetableDetails(models.Model):
    objects = models.Manager

    timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, limit_choices_to={'is_active': True})

    class Meta:
        verbose_name_plural = "Timetable Details"
        verbose_name = "Timetable Details"

    def __str__(self):
        return str(self.timetable.start_time)


class Enquiry(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150)
    mobile_no = models.CharField(max_length=10)
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    remarks = models.TextField()
    date = models.DateField(default=datetime.now, null=True, blank=True)

    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True})

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Enquiries"
        verbose_name = "Enquiry"

    def __str__(self):
        return self.name


class Rank(models.Model):
    objects = models.Manager

    date = models.DateField(default=datetime.now)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    rank_type = models.ForeignKey(
        RankType, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    points = models.IntegerField(default=0)

    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True})

    # Default Column Name
    # is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Ranks"
        verbose_name = "Rank"

    def __str__(self):
        return self.student.name


class Attendance(models.Model):
    objects = models.Manager

    # class type(models.IntegerChoices):
    #     PRESENT = 0
    #     ABSENT = 1
    #     LEAVE = 2

    date = models.DateField(default=datetime.now)
    # student = models.ForeignKey(
    #     Student, on_delete=models.CASCADE, limit_choices_to={'is_active': True}, default=1)
    timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)

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


class AttendanceDetails(models.Model):
    objects = models.Manager

    class type(models.IntegerChoices):
        PRESENT = 1
        ABSENT = 2
        LEAVE = 3

    attendance = models.ForeignKey(
        Attendance, on_delete=models.CASCADE, limit_choices_to={'is_active': True}, default=1)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    is_present = models.IntegerField(
        choices=type.choices, default=type.PRESENT)
    remarks = models.TextField(null=True, blank=True, default='')

    def is_present_str(self):
        if self.is_present == 1:
            return 'P'
        elif self.is_present == 2:
            return 'A'
        elif self.is_present == 3:
            return 'L'

    class Meta:
        verbose_name_plural = "Attendance Details"
        verbose_name = "Attendance Details"

    def __str__(self):
        return self.student.name


class LeaveRequest(models.Model):
    objects = models.Manager

    class status_(models.IntegerChoices):
        PENDING = 0
        APPROVED = 1
        REJECTED = 2

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    date = models.DateField(default=datetime.now)
    remarks = models.TextField(null=True, blank=True, default='')
    status = models.IntegerField(
        choices=status_.choices, default=status_.PENDING, null=True, blank=True)

    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True})

    # Default Column Name
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    def get_status(self):
        if self.status == 1:
            return 'Approved'
        elif self.status == 2:
            return 'Rejected'
        else:
            return 'Pending'

    class Meta:
        verbose_name_plural = "Leave Requests"
        verbose_name = "Leave Request"

    def __str__(self):
        return self.student.name
