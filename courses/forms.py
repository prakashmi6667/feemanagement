from django import forms
from .models import AssignCourse,Course
from django.db.models import F


class AssignCourseForm(forms.ModelForm):

    class Meta:
        model = AssignCourse
        fields = "__all__"
        
    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        franchise__id = self.request.session['LoggedInFranchise']['franchise__pk']
        super(AssignCourseForm, self).__init__(*args, **kw)
        


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = "__all__"
        
    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        franchise__id = self.request.session['LoggedInFranchise']['franchise__pk']
        super(CourseForm, self).__init__(*args, **kw)
        
