from django.contrib import admin
from .models import FeeStatus, FeeInstallment, Fees
from .forms import FeeInstallmentForm
from students.models import Student
from django.utils.html import format_html
# Register your models here.


class FeeStatusAdmin(admin.ModelAdmin):
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


class FeeInstallmentAdmin(admin.ModelAdmin):
    form = FeeInstallmentForm
    list_display = ['student', 'course', 'fee_amount', 'discount', 'total_amount',
                    'monthly_amount', 'total_installment', 'franchise', 'created_by', 'created_on']
    list_filter = ['created_by', 'created_on']
    list_per_page = 10
    search_fields = ['student__name']

    actions = ["active_selected_record", 'inactive_selected_record']

    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

    class Media:
        js = (
        "js/jquery.js",
        "lib/helper.js",
        )








class FeesAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'receipt_no', 'fee', 'discount', 'total_amount',
                    'paid_amount', 'fine', 'franchise', 'recept_print','created_by', 'created_on']
    list_filter = ['created_by', 'created_on']
    list_per_page = 10
    search_fields = ['student__name']

    actions = ["active_selected_record", 'inactive_selected_record']

    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

    def recept_print(self,obj):
        return format_html(f"<a href='/fees/recept/print/{obj.id}/' target='_blank'>print</a>")



admin.site.register(FeeStatus, FeeStatusAdmin)
admin.site.register(FeeInstallment, FeeInstallmentAdmin)
admin.site.register(Fees, FeesAdmin)