from django.contrib import admin
# from .models import Designation, Employee, EmpAttendance, EmpAttendanceDetails
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter,DropdownFilter
# Register your models here.


# class DesignationAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created_by', 'created_on']
#     list_filter = ['created_by', 'created_on']
#     list_per_page = 10
#     search_fields = ['name']

#     actions = ["active_selected_record", 'inactive_selected_record']

#     def active_selected_record(self, request, queryset):
#         queryset.update(is_active=True)

#     def inactive_selected_record(self, request, queryset):
#         queryset.update(is_active=False)

#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user

#         super().save_model(request, obj, form, change)


# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ['name', 'email', 'password',
#                     'mobile_no', 'franchise', 'is_active']
#     list_filter = (('franchise',RelatedDropdownFilter),)
#     list_per_page = 10
#     search_fields = ['name']
#     list_editable = ['email', 'password']

#     actions = ["active_selected_record", 'inactive_selected_record']

#     def active_selected_record(self, request, queryset):
#         queryset.update(is_active=True)

#     def inactive_selected_record(self, request, queryset):
#         queryset.update(is_active=False)

#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user

#         super().save_model(request, obj, form, change)


# class EmpAttendanceAdmin(admin.ModelAdmin):
#     list_display = ['date', 'franchise',
#                     'created_by', 'created_on']
#     list_filter = ['created_by', 'created_on']
#     list_per_page = 10
#     search_fields = ['franchise__name']

#     actions = ["active_selected_record", 'inactive_selected_record']

#     def active_selected_record(self, request, queryset):
#         queryset.update(is_active=True)

#     def inactive_selected_record(self, request, queryset):
#         queryset.update(is_active=False)

#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user

#         super().save_model(request, obj, form, change)


# class EmpAttendanceDetailsAdmin(admin.ModelAdmin):
#     list_display = ['attendance', 'employee', 'is_present', 'remarks']
#     list_filter = ['attendance']
#     list_per_page = 10
#     search_fields = ['employee__name']

#     actions = ["active_selected_record", 'inactive_selected_record']

#     def active_selected_record(self, request, queryset):
#         queryset.update(is_active=True)

#     def inactive_selected_record(self, request, queryset):
#         queryset.update(is_active=False)

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)


# admin.site.register(Designation, DesignationAdmin)
# admin.site.register(Employee, EmployeeAdmin)
# admin.site.register(EmpAttendance, EmpAttendanceAdmin)
# admin.site.register(EmpAttendanceDetails, EmpAttendanceDetailsAdmin)
