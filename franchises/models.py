from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth import settings
from courses.models import Duration
# Create your models here.


# Create your models here.
def max_Code1():
    Is_code =  Franchise.objects.all().count()
    
    if Is_code>0 :
        obj = Franchise.objects.all().order_by('-id')[0]
        st_code = obj.code
        st_code = st_code[4:]
        st_code = int(st_code)
        st_code+=1
       
        var = 'UTEC'+str(st_code).zfill(4)
        return var
    else:
        
        code = 'UTEC'
        return code+'0101'

def max_code(account_id):
    maxcount = 100
    Is_code = Franchise.objects.get(pk=account_id)
    if not Is_code.code:
        obj = Franchise.objects.all().count()
        maxcount += (obj+1)
        return 'UTEC'+str(maxcount).zfill(4)
    else:
        return Is_code.code


class InstituteType(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Institute Types"
        verbose_name = "Institute Type"

    def __str__(self):
        return self.name


class Refrence(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Refrences"
        verbose_name = "Refrence"

    def __str__(self):
        return self.name


class Franchise(models.Model):
    objects = models.Manager

    class options(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX_OR_MORE = 6

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=150, editable=False,
                            unique=True, null=True, blank=True)
    email = models.EmailField(max_length=150)
    mobile_no = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=15, null=True, blank=True)
    institute_type = models.ForeignKey(
        InstituteType, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    establishment_year = models.CharField(max_length=10)
    address = models.TextField()
    state = models.ForeignKey(
        'settings.state', on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    district = models.ForeignKey(
        'settings.District', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    city = models.CharField(max_length=150)
    post_office = models.CharField(max_length=150, null=True, blank=True)
    police_station = models.CharField(max_length=150, null=True, blank=True)
    pin_code = models.CharField(max_length=150)
    gst_no = models.CharField(max_length=150, null=True, blank=True)
    privacy_policy = models.BooleanField(default=False, null=True, blank=True)
    is_internet = models.BooleanField(default=False, null=True, blank=True)
    is_inverter = models.BooleanField(default=False, null=True, blank=True)
    is_drinking_water = models.BooleanField(
        default=True, null=True, blank=True)
    computers = models.IntegerField(
        choices=options.choices, default=options.ZERO, null=True, blank=True)
    refrence_books = models.IntegerField(
        choices=options.choices, default=options.ZERO, null=True, blank=True)
    licensed_software = models.IntegerField(
        choices=options.choices, default=options.ZERO, null=True, blank=True)
    journal = models.IntegerField(
        choices=options.choices, default=options.ZERO, null=True, blank=True)
    cd = models.IntegerField(choices=options.choices,
                             default=options.ZERO, null=True, blank=True)
    projector = models.IntegerField(
        choices=options.choices, default=options.ZERO, null=True, blank=True)

    plan = models.ForeignKey(
        'settings.Plan', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    amount = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.ForeignKey(
        'settings.PaymentMethod', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    payment_reciept = models.ImageField(
        upload_to='franchise/', max_length=150, null=True, blank=True)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    order_id = models.CharField(max_length=200, null=True, blank=True)
    signature = models.CharField(max_length=200, null=True, blank=True)

    refrence_from = models.ForeignKey(
        Refrence, on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    refrence_code = models.CharField(max_length=200, null=True, blank=True)

    center_head_image = models.ImageField(
        upload_to='franchise/', max_length=150)
    voter_id_card_image = models.ImageField(
        upload_to='franchise/', max_length=150, null=True, blank=True)
    pan_card_image = models.ImageField(
        upload_to='franchise/', max_length=150, null=True, blank=True)
    certificate_image = models.ImageField(
        upload_to='franchise/', max_length=150, null=True, blank=True)
    theory_room_image = models.ImageField(
        upload_to='franchise/', max_length=150, null=True, blank=True)
    practical_room_image = models.ImageField(
        upload_to='franchise/', max_length=150, null=True, blank=True)
    office_room_image = models.ImageField(
        upload_to='franchise/', max_length=150, null=True, blank=True)
    front_side_image = models.ImageField(
        upload_to='franchise/', max_length=150, null=True, blank=True)
    signature_image = models.ImageField(
        upload_to='franchise/', max_length=150, null=True, blank=True)
    is_approved = models.BooleanField(default=False, null=True, blank=True)
    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Franchises"
        verbose_name = "Franchise"

    def __str__(self):
        if self.code:
            return self.name.capitalize()[0:15]+'... '+self.code
        else:
            return self.name.capitalize()[0:15]

class Franchise_Rank(models.Model):
    objects = models.Manager

    date = models.DateField(default=datetime.now)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    points = models.IntegerField(default=0)
    duration = models.ForeignKey(Duration,on_delete=models.CASCADE,limit_choices_to={'is_active':True})

   

    # Default Column Name
    # is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Franchise Ranks"
        verbose_name = "Franchise Rank"

    def __str__(self):
        return self.franchise.name

class MessageBoard(models.Model):
    objects = models.Manager

    franchise = models.ForeignKey(
        Franchise, on_delete=models.CASCADE)
    message = models.TextField()
    revert_message = models.TextField()

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Message Boards"
        verbose_name = "Message Board"

    def __str__(self):
        return self.franchise.name
