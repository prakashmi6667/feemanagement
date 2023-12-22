from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth import settings

# Create your models here.

def reccipt_code():
    code=0
    fee =  Fees.objects.all().count()
    if fee>0:
        code+=1
        fees_code='REC'+ str(code).zfill(3)
        return fees_code
    else:
        return 'REC001'




class FeeStatus(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True) 
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Fee Status"
        verbose_name = "Fee Status"

    def __str__(self):
        return self.name


class FeeInstallment(models.Model):
    objects = models.Manager

    student = models.ForeignKey(
        'students.Student', on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, null=True, blank=True)
    fee_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, help_text="Discount should be in amount!")
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    monthly_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    total_installment = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)

    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    status = models.ForeignKey(
        FeeStatus, on_delete=models.CASCADE, limit_choices_to={'is_active': True})

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    def get_installment(self):
        tot = FeeInstallment.objects.get(student=self.student)
        inst = Fees.objects.filter(student=self.student).count()
        tot = tot.total_installment

        return str(inst)+'/'+str(tot)

    def is_last_installment(self):
        inst = 0
        tot = FeeInstallment.objects.get(student=self.student)
        inst = Fees.objects.filter(student=self.student).count()
        tot = tot.total_installment

        
        rst = tot-inst
        

        if rst == 1:
            return True
        else:
            return False

    def is_last_installment_len(self):
        inst = 0
        rst=0
        tot = FeeInstallment.objects.get(student=self.student)
        inst = Fees.objects.filter(student=self.student).count()
        tot = tot.total_installment

        if inst>0:
            rst = tot-inst
            print(rst)

        if inst==0:
            return True
        elif rst <= tot:
            if rst==0:
                return False
               
            else:
                return True
            # return True
        else:
            return True

    class Meta:
        verbose_name_plural = "Fee Installments"
        verbose_name = "Fee Installment"

    def __str__(self):
        return self.student.name


class Fees(models.Model):
    objects = models.Manager

    student = models.ForeignKey(
        'students.Student', on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    receipt_no = models.CharField(max_length=150)
    date = models.DateField(default=datetime.now)
    fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    fine = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    remarks = models.TextField(null=True, blank=True)

    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    status = models.ForeignKey(
        FeeStatus, on_delete=models.CASCADE, limit_choices_to={'is_active': True}, default=2)

    payment_method = models.ForeignKey(
        'settings.PaymentMethod', on_delete=models.CASCADE, limit_choices_to={'is_active': True}, default=1)
    payment_reciept = models.ImageField(
        upload_to='fees/', max_length=150, null=True, blank=True)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    order_id = models.CharField(max_length=200, null=True, blank=True)
    signature = models.CharField(max_length=200, null=True, blank=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    def pending_amount(self):
        return self.total_amount-self.paid_amount

    def is_pending_amount(self):
        tot = self.total_amount-self.paid_amount
        if tot > 0:
            return True
        else:
            return False

    def get_installment(self):
        tot = FeeInstallment.objects.get(student=self.student)
        inst = Fees.objects.filter(student=self.student).count()
        tot = tot.total_installment

        return str(inst)+'/'+str(tot)

    def is_last_installment(self):
      
        tot = FeeInstallment.objects.get(student=self.student)
        inst = Fees.objects.filter(student=self.student).count()
        tot = tot.total_installment


        rst = tot-inst

        if rst == 1:
            return True
        else:
            return False

    class Meta:
        verbose_name_plural = "Fees"
        verbose_name = "Fees"

    def __str__(self):
        return self.student.name

    def is_last_installment_len(self):
        inst = 0
        rst=0
        tot = FeeInstallment.objects.get(student=self.student)
        inst = Fees.objects.filter(student=self.student).count()
        tot = tot.total_installment

        if inst>0:
            rst = tot-inst

        if rst >= 1:
            return True
        else:
            return False
