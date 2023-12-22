from django.contrib import admin
from .models import Student, Category, Religion, Qualification
from .models import EnquirySource, Days, Timetable, Rank, RankType, Enquiry, Attendance, TimetableDetails, AttendanceDetails, LeaveRequest,max_St_Code,Facilities,Other_Facilities
from django_admin_listfilter_dropdown.filters import DropdownFilter,RelatedDropdownFilter,ChoiceDropdownFilter
from settings.forms import OnchangeDistrictbystateForm

from employees.models import Employee
from franchises.models import Franchise

# Register your models here.
class Otherfacilites(admin.StackedInline):
    model = Other_Facilities
    extra = 1


class FacilitiesAdmin(admin.ModelAdmin):
    list_display = ['name','price', 'created_by', 'created_on']
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

class OtherFacilitiesAdmin(admin.ModelAdmin):
    list_display = ['student','facilities', 'created_by', 'created_on']
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

class StudentAdmin(admin.ModelAdmin):
    form = OnchangeDistrictbystateForm
    inlines = [Otherfacilites]
    list_display = ['name', 'code', 'email', 'password', 'course', 'gender', 'is_certified',
                    'marital_status', 'father_name', 'dob', 'franchise', 'is_active']

    # list_filter = (('gender', DropdownFilter), ('is_active', DropdownFilter), ('is_drop_out', ChoiceDropdownFilter),
    #                ('is_certified', DropdownFilter), ('enquiry_source', RelatedDropdownFilter), ('franchise', RelatedDropdownFilter),)
    list_filter=['gender','is_certified']
    list_per_page = 50
    search_fields = ['name', 'course__code']
    list_editable = ['email', 'password']
    date_hierarchy = 'join_date'

    actions = ["active_selected_record", 'inactive_selected_record']
    

    class Media:
        js = (
            "js/jquery.min.js",
            "lib/helper.js",
            "lib/change.js",
        )
    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.code = max_St_Code(obj.franchise.pk)
            obj.created_by = request.user
        
        super().save_model(request, obj, form, change)

        # print('Init ----------------')

        # students = Student.objects.all()

        # for st in students:
        #     st.mobile_no = '9837994101'
        #     st.address = 'Near Bharat Gas Agency, Dineshpur, Uttarakhand'
        #     st.save()
        # print('Student Done ----------------')

        # employees = Employee.objects.all()

        # for emp in employees:
        #     emp.mobile_no = '9837994101'
        #     emp.address = 'Near Bharat Gas Agency, Dineshpur, Uttarakhand'
        #     emp.save()
        
        # print('Employee Done ----------------')

        # franchise = Franchise.objects.all()

        # for fr in franchise:
        #     fr.mobile_no = '9837994101'
        #     fr.address = 'Near Bharat Gas Agency, Dineshpur, Uttarakhand'
        #     fr.save()
        
        # print('Franchise Done ----------------')

        


class CategoryAdmin(admin.ModelAdmin):
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


class ReligionAdmin(admin.ModelAdmin):
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


class QualificationAdmin(admin.ModelAdmin):
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


class EnquirySourceAdmin(admin.ModelAdmin):
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


class DaysAdmin(admin.ModelAdmin):
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


class TimetableDetailsInlines(admin.StackedInline):
    model = TimetableDetails
    extra = 1


class TimetableAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'name',  'view_days',
                    'course', 'franchise', 'total_students']
    list_filter = ['start_time', 'end_time', 'days', 'franchise', ]
    list_per_page = 100
    # search_fields = ['name']
    inlines = [TimetableDetailsInlines]

    actions = ["active_selected_record", 'inactive_selected_record']

    def total_students(self, obj):
        return TimetableDetails.objects.filter(timetable__pk=obj.pk, student__is_active=True).count()

    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)


class TimetableDetailsAdmin(admin.ModelAdmin):
    list_display = ['timetable', 'student']
    list_filter = ['student__is_active', 'timetable']


class RankTypeAdmin(admin.ModelAdmin):
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


class RankAdmin(admin.ModelAdmin):
    list_display = ['student', 'created_by', 'created_on']
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


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile_no', 'course',
                    'remarks', 'franchise', 'created_by', 'created_on']
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


class AttendanceDetailsInlines(admin.StackedInline):
    model = AttendanceDetails
    extra = 1


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['date', 'timetable',
                    'present_count', 'absent_count', 'franchise']
    list_filter = ['timetable', 'franchise']
    list_per_page = 31
    date_hierarchy = 'date'
    search_fields = ['franchise__name']
    inlines = [AttendanceDetailsInlines]

    actions = ["active_selected_record", 'inactive_selected_record']

    def present_count(self, obj):
        return AttendanceDetails.objects.filter(attendance__pk=obj.pk, is_present=1).count()

    def absent_count(self, obj):
        return AttendanceDetails.objects.filter(attendance__pk=obj.pk, is_present=2).count()

    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)


class AttendanceDetailsAdmin(admin.ModelAdmin):
    list_display = ['attendance', 'student', 'is_present', 'remarks']


class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'date',
                    'remarks', 'status', 'franchise', 'created_by', 'created_on']
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


admin.site.register(Student, StudentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Religion, ReligionAdmin)
admin.site.register(Qualification, QualificationAdmin)
# admin.site.register(EnquirySource, EnquirySourceAdmin)
# admin.site.register(Days, DaysAdmin)
# admin.site.register(Timetable, TimetableAdmin)
# admin.site.register(Rank, RankAdmin)
# admin.site.register(RankType, RankTypeAdmin)
# admin.site.register(Enquiry, EnquiryAdmin)
# admin.site.register(Attendance, AttendanceAdmin)
# admin.site.register(TimetableDetails, TimetableDetailsAdmin)
# admin.site.register(AttendanceDetails, AttendanceDetailsAdmin)
# admin.site.register(LeaveRequest, LeaveRequestAdmin)
admin.site.register(Facilities, FacilitiesAdmin)
admin.site.register(Other_Facilities, OtherFacilitiesAdmin)
