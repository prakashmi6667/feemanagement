from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
# from django.conf.urls import url
from django.urls import include, re_path
from .models import InstituteType, Refrence, Franchise, max_code, MessageBoard,max_Code1,Franchise_Rank
# from django_admin_listfilter_dropdown.filters import DropdownFilter,RelatedDropdownFilter
from accounts.models import Wallet
from settings.forms import OnchangeDistrictbystateForm
# Register your models here.


class InstituteTypeAdmin(admin.ModelAdmin):
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


class RefrenceAdmin(admin.ModelAdmin):
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


class FranchiseAdmin(admin.ModelAdmin):
    form = OnchangeDistrictbystateForm
    list_display = ['is_active', 'name', 'code', 'mobile_no',
                    'state', 'district', 'status', 'plan', 'certificate']
    # list_filter = (('name',DropdownFilter),('is_approved',DropdownFilter),('is_active',DropdownFilter),
                #   ('plan',RelatedDropdownFilter),('institute_type',RelatedDropdownFilter),('state',RelatedDropdownFilter) )
    list_filter = ['name','plan','institute_type']
    list_per_page = 50
    search_fields = ['name', 'code']
    list_editable = ['plan']
    list_display_links = ['name', ]

    fieldsets = (
        (None, {
            'fields': (('name', 'email', 'mobile_no'), ('institute_type', 'establishment_year', 'gst_no'),)
        }),
        ('Address Details', {
            'classes': ('collapse',),
            'fields': (('address', 'state', 'district', 'city', 'post_office', 'police_station', 'pin_code'),),
        }),
        ('Office Details', {
            'classes': ('collapse',),
            'fields': (('is_internet', 'is_inverter', 'is_drinking_water', 'computers', 'cd'),
                       ('journal', 'refrence_books', 'licensed_software', 'projector'))
        }),
        ('Franchise Plan Details', {
            'classes': ('collapse',),
            'fields': (('plan', 'amount', 'order_id', 'signature'),)
        }),
        ('Image Details', {
            'classes': ('collapse',),
            'fields': (('center_head_image', 'voter_id_card_image', 'pan_card_image', 'certificate_image'),
                       ('theory_room_image', 'practical_room_image',
                        'office_room_image', 'front_side_image'),
                       'signature_image')
        }),
        (None, {
            'classes': (),
            'fields': (('privacy_policy', 'refrence_from', 'refrence_code', 'is_approved'),)
        }),
    )

    class Media:
        js = (
            "js/jquery.js",
            "lib/district.js",
        )

    def certificate(self, obj):
        return format_html(f'<a class="button" href="/franchise/print/{obj.id}/" target="_blank">Certificate</a>')

    def activateAccount(self, request, account_id, *args, **kwargs):
        obj = Franchise.objects.get(pk=account_id)
        code = max_code(account_id)
        if code:
            obj.code = code
            obj.is_approved = True
        obj.save()

        return redirect(reverse('admin:franchises_franchise_changelist'))

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^(?P<account_id>.+)/activate/$',
                self.admin_site.admin_view(self.activateAccount),
                name='activate',
            ),
        ]
        return custom_urls + urls

    def status(self, obj):
        if(obj.is_approved):
            return 'Approved'
        else:
            return format_html(
                '<a class="button" href="{}">Activate</a>',
                reverse('admin:activate', args=[obj.pk]),
            )

    status.empty_value_display = 'NA'

    actions = ["active_selected_record", 'inactive_selected_record']

    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.code = max_Code1()
            obj.created_by = request.user

        super().save_model(request, obj, form, change)
        if not change:
            Wallet.objects.create(amount=0,franchise=obj)


class FranchiseRankAdmin(admin.ModelAdmin):
    list_display = ['franchise','points','duration','created_by', 'created_on']
    list_filter = ['created_by', 'created_on']
    list_per_page = 10
    search_fields = ['franchise__name','duration']

    actions = ["active_selected_record", 'inactive_selected_record']

    def active_selected_record(self, request, queryset):
        queryset.update(is_active=True)

    def inactive_selected_record(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)



class MessageBoardAdmin(admin.ModelAdmin):
    list_display = ['franchise', 'message',
                    'revert_message', 'created_by', 'created_on']
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


admin.site.register(InstituteType, InstituteTypeAdmin)
# admin.site.register(Refrence, RefrenceAdmin)
admin.site.register(Franchise, FranchiseAdmin)
# admin.site.register(MessageBoard, MessageBoardAdmin)
# admin.site.register(Franchise_Rank,FranchiseRankAdmin)
