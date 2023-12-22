from django.contrib import admin
from .models import Duration, Course, AssignCourse
from django_admin_listfilter_dropdown.filters import DropdownFilter,RelatedDropdownFilter
# Register your models here.


class DurationAdmin(admin.ModelAdmin):
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


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'duration',
                    'is_active']
    list_filter = (('name',DropdownFilter),('duration',RelatedDropdownFilter),( 'is_active',DropdownFilter))
    list_per_page = 50
    search_fields = ['name', 'code']

    actions = ["active_selected_record", 'inactive_selected_record']

    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)


class AssignCourseAdmin(admin.ModelAdmin):
    list_display = ['franchise', 'course', 'fee', 'created_on']
    list_filter = ['created_by', 'created_on', 'course']
    list_per_page = 10
    search_fields = ['franchise__name']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)


admin.site.register(Course, CourseAdmin)
admin.site.register(Duration, DurationAdmin)
admin.site.register(AssignCourse, AssignCourseAdmin)
