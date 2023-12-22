from django.contrib import admin
from .models import WalletStatus, Wallet, WalletTransaction
from django.contrib import messages
import os
# Register your models here.


class WalletStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_on']
    list_filter = ['created_by', 'created_on']
    list_per_page = 10
    search_fields = ['name']

    actions = ["active_selected_record", 'inactive_selected_record']

    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)


class WalletAdmin(admin.ModelAdmin):
    list_display = ['amount', 'franchise']
    list_filter = ['franchise']
    list_per_page = 10
    search_fields = ['franchise__name']

    actions = ["active_selected_record", 'inactive_selected_record']

    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)


class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'date', 'payment_method', 'status',
                    'transaction_type', 'franchise', 'created_by', 'created_on']
    list_filter = ['created_by', 'created_on']
    list_per_page = 10
    search_fields = ['name']
    list_editable = ['status']

    actions = ["active_selected_record", 'inactive_selected_record']

    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)

    def save_formset(self, request, form, formset, change):
        # get all the objects in the formset
        instances = formset.save(commit=False)

        for instance in instances:
            # do something ...
            obj= instance
            objwall = Wallet.objects.filter(franchise=obj.franchise)

            if len(objwall)<=0:
                Wallet.objects.create(amount=obj.amount, franchise=obj.franchise)

            if obj.transaction_type == 1: # Withdrawal
                if len(objwall)>0:
                    objwall = objwall[0]
                    if obj.status.pk==1: # Approved
                        objwall.amount = objwall.amount - obj.amount
                        objwall.save()
                    else:
                        objwall.amount = objwall.amount + obj.amount
                        objwall.save()

            else: # Deposit
                if len(objwall)>0:
                    objwall = objwall[0]
                    if obj.status.pk==1: # Approved
                        objwall.amount = objwall.amount + obj.amount
                        objwall.save()
                    else:
                        objwall.amount = objwall.amount - obj.amount
                        objwall.save()

            instance.save()
            messages.add_message(request, messages.success, 'success!')

    def save_model(self, request, obj, form, change):
        try:
            objwall = Wallet.objects.filter(franchise=obj.franchise)

            if len(objwall)<=0:
                Wallet.objects.create(amount=obj.amount, franchise=obj.franchise)

            if obj.transaction_type == 1: # Withdrawal
                if len(objwall)>0:
                    objwall = objwall[0]
                    if obj.status.pk==1: # Approved
                        objwall.amount = objwall.amount - obj.amount
                        objwall.save()
                    else:
                        objwall.amount = objwall.amount + obj.amount
                        objwall.save()
            else: # Deposit
                if len(objwall)>0:
                    objwall = objwall[0]
                    if obj.status.pk==1: # Approved
                        objwall.amount = objwall.amount + obj.amount
                        objwall.save()
                    else:
                        objwall.amount = objwall.amount - obj.amount
                        objwall.save()

            if not change:
                obj.created_by = request.user
            super().save_model(request, obj, form, change)

        except Exception as error:
            print(error)
            
    def delete_model(self,request,obj):
        try:
            objwall = Wallet.objects.filter(franchise=obj.franchise)

            if obj.transaction_type == 1: # Withdrawal
                if len(objwall)>0:
                    objwall = objwall[0]
                    if obj.status.pk==1: # Approved
                        objwall.amount = objwall.amount + obj.amount
                        objwall.save()
                    else:
                        objwall.amount = objwall.amount - obj.amount
                        objwall.save()
            else: # Deposit
                if len(objwall)>0:
                    objwall = objwall[0]
                    if obj.status.pk==1: # Approved
                        objwall.amount = objwall.amount - obj.amount
                        objwall.save()
                    else:
                        objwall.amount = objwall.amount + obj.amount
                        objwall.save()


            os.remove(obj.image.path)
            super().delete_model(request, obj)
        except Exception as er:
            print(er)
    
    def delete_queryset(self, request, queryset):
        try:
            for obj in queryset:
                
                objwall = Wallet.objects.filter(franchise=obj.franchise)
                if obj.transaction_type == 1: # Withdrawal
                        if len(objwall)>0:
                            objwall = objwall[0]
                            if obj.status.pk==1: # Approved
                                objwall.amount = objwall.amount + obj.amount
                                objwall.save()
                            # else:
                            #     objwall.amount = objwall.amount - obj.amount
                            #     objwall.save()

                else: # Deposit
                    if len(objwall)>0:
                        objwall = objwall[0]
                        if obj.status.pk==1: # Approved
                            objwall.amount = objwall.amount - obj.amount
                            objwall.save()
                        # else:
                        #     objwall.amount = objwall.amount + obj.amount
                        #     objwall.save()

            queryset.delete()
        except Exception as error:
            print(error)

    

admin.site.register(WalletStatus, WalletStatusAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
