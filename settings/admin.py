from django.contrib import admin
from .models import State, District, Plan, Tinify, PaymentMethod
from django_admin_listfilter_dropdown.filters import DropdownFilter,RelatedDropdownFilter

# Register your models here.


class DistrictInline(admin.StackedInline):
    model = District
    extra = 1


class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_on']
    list_filter = ['created_by', 'created_on']
    list_per_page = 100
    search_fields = ['name']
    inlines = [DistrictInline]

    actions = ["active_selected_record", 'inactive_selected_record']

    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'created_by', 'created_on']
    # list_filter = (('name',DropdownFilter),('state',RelatedDropdownFilter), ('created_on',DropdownFilter))
    list_filter = ['name','state']
    list_per_page = 50
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


class TinifyAdmin(admin.ModelAdmin):
    list_display = ['name', 'api_key', 'count', 'created_by', 'created_on']
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


class PlanAdmin(admin.ModelAdmin):
    list_display = ['name','details','price','created_by', 'created_on']
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


class PaymentMethodAdmin(admin.ModelAdmin):
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


admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
# admin.site.register(Plan, PlanAdmin)
# admin.site.register(Tinify, TinifyAdmin)




# DELETE FROM settings_plan;
# DELETE FROM sqlite_sequence WHERE name = 'settings_plan';