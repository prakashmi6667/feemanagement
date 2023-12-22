from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth import settings

# Create your models here.


class WalletStatus(models.Model):
    objects = models.Manager

    name = models.CharField(max_length=150, unique=True)

    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = "Wallet Status"
        verbose_name = "Wallet Status"

    def __str__(self):
        return self.name


class Wallet(models.Model):
    objects = models.Manager

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True})

    class Meta:
        verbose_name_plural = "Wallet"
        verbose_name = "Wallet"

    def __str__(self):
        return str(self.amount)


class WalletTransaction(models.Model):
    objects = models.Manager

    class transaction_type(models.IntegerChoices):
        Withdraw = 1
        Deposit = 3

    name = models.CharField(max_length=150, verbose_name='Name')
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    date = models.DateField(default=datetime.now)
    payment_method = models.ForeignKey(
        'settings.PaymentMethod', on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    payment_reciept = models.ImageField(
        upload_to='fees/', max_length=150, null=True, blank=True)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    order_id = models.CharField(max_length=200, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    signature = models.CharField(max_length=200, null=True, blank=True)
    status = models.ForeignKey(
        WalletStatus, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    transaction_type = models.IntegerField(
        choices=transaction_type.choices, default=transaction_type.Deposit)
    franchise = models.ForeignKey(
        'franchises.Franchise', on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    # Default Column Name
    is_active = models.BooleanField(default=True, editable=False)
    created_on = models.DateField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    modified_on = models.DateField(default=datetime.now, editable=False)

    def get_transaction_type_str(self):
        if self.transaction_type == 1:
            return 'Withdraw'
        else:
            return 'Deposit'

    class Meta:
        verbose_name_plural = "Wallet Transactions"
        verbose_name = "Wallet Transaction"

    def __str__(self):
        return self.franchise.name
