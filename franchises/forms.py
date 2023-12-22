from django import forms
# from django.forms import formset_factory
# from django.forms import inlineformset_factory, modelformset_factory
from .models import Franchise, MessageBoard
# from employees.forms import CenterHeadInlineFormset, CenterHeadInlineForm, EmployeeInlineFormSet, EmployeeInlineForm
# from employees.models import Employee as CenterHead
# from employees.models import Employee as Employee


class franchiseForm(forms.ModelForm):
    # CenterHead = inlineformset_factory(
    #     Franchise, CenterHead, formset=CenterHeadBaseInlineFormSet, fields=('__all__'), exclude=('religion', 'nationality',), max_num=1, extra=1, can_delete=False)

    # CenterHead = formset_factory(
    #     CenterHeadInlineForm, max_num=1, extra=1, can_delete=False)
    # Employee = formset_factory(EmployeeInlineForm, extra=1, can_delete=True)

    # Employee = inlineformset_factory(
    #     Franchise, Employee, formset=EmployeeInlineFormSet, fields=('name', 'gender', 'job_Type', 'experience',), extra=1, can_delete=False)

    # CenterHeadInlineFormset = modelformset_factory(Employee, formset=CenterHeadInlineFormset,
    #                                                form=CenterHeadInlineForm, max_num=1, extra=1, can_delete=False)
    # EmployeeInlineFormset = modelformset_factory(Employee, formset=EmployeeInlineFormSet,
    #                                              form=EmployeeInlineForm, extra=2, can_delete=False)

    class Meta:
        model = Franchise
        fields = "__all__"
        exclude = ('is_approved', 'payment_id', 'order_id', 'code', 'payment_method',
                   'signature', 'privacy_policy', 'plan', 'amount')

    def __init__(self, *args, **kw):
        super(franchiseForm, self).__init__(*args, **kw)
        self.fields['center_head_image'].required = False
        self.fields['voter_id_card_image'].required = False
        self.fields['pan_card_image'].required = False
        self.fields['certificate_image'].required = False
        self.fields['theory_room_image'].required = False
        self.fields['practical_room_image'].required = False
        self.fields['office_room_image'].required = False
        self.fields['front_side_image'].required = False
        self.fields['signature_image'].required = False

    # def clean(self):
    #     cleaned_data = super(franchiseForm, self).clean()


class MessageBoardForm(forms.ModelForm):

    class Meta:
        model = MessageBoard
        fields = "__all__"
        exclude = ('franchise', 'revert_message')
        # widgets = {
        #     'student': forms.Select(attrs={'onChange': 'fn_GetCourse()'}),
        #     'course': forms.Select(attrs={'disabled': 'disabled'}),
        # }

    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        franchise__id = self.request.session['LoggedInFranchise']['franchise__pk']

        super(MessageBoardForm, self).__init__(*args, **kw)
        # self.fields["student"].queryset = Student.objects.filter(
        #     is_active=True, franchise__pk=franchise__id)

class FranchiseOnchangeForm(forms.ModelForm):
    
    class Meta:
        model = Franchise
        fields = "__all__"
        widgets = {'state':forms.Select(attrs={'onchange':'fn_GetDistrict()'})}
