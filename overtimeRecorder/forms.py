from django import forms
from .models import OvertimeRow, Profile, Roster
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
col_control = 'form-control col-sm-6'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = col_control
        self.fields["email"].widget.attrs["readonly"] = True
        self.fields["email"].help_text = "this is linked to your username and isn't editable. Please contact admin if you need this changed"

class CreateNewUserForm(UserCreationForm):
    first_name= forms.CharField()
    last_name= forms.CharField()
    email= forms.CharField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    def __init__(self, *args, **kwargs):
        super(CreateNewUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = col_control
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('employeeNumber','classification', 'department', 'payCycle', 'okToShareRoster', 'okToShareOvertime')
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = col_control


class OvertimeRowForm(forms.ModelForm):
    class Meta:
        model = OvertimeRow
        fields = ('date', 'reason', 'patientURN','startTime', 'finishTime', 'higherDutiesYN','preApproval','personalComment')
    
    
    def __init__(self, *args, **kwargs):
        super(OvertimeRowForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = col_control
            
    widgets = {
        "startTime": forms.TimeInput(format='%H:%M'),
        "finishTime": forms.TimeInput(format='%H:%M')
    }

class OvertimeRowFormShortened(forms.ModelForm):
    class Meta:
        model = OvertimeRow
        fields = ('date', 'reason', 'patientURN','startTime', 'finishTime','personalComment')
        
    def __init__(self, *args, **kwargs):
        super(OvertimeRowFormShortened, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = col_control

class OvertimeRowFormSuperShortened(forms.Form):
    CLINICAL_REASONS = (
        ('', "Reason") ,
        (1, "Direct Patient Care or Theatre") ,
        (2, "WR or Delayed/Extended handover (no URN)"),
        (3, "Discharge Summaries or Patient Admin"),
        (4, "MDM preparation"),
    )
    reason = forms.ChoiceField(label="Reason for overtime", choices=CLINICAL_REASONS, required=False)
    patientURN = forms.CharField(label="Patient URN", max_length=20, required=False)
    arriveEarly = forms.TimeField(label="Early time", required=False)
    leaveLate = forms.TimeField(label="Late time", required=False)
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    def __init__(self, *args, **kwargs):
        super(OvertimeRowFormSuperShortened, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control-sm form-control small-form-css col'
            visible.field.widget.attrs['placeholder'] = visible.field.label


class RosterForm(forms.Form):
    rosterField = forms.CharField(label="Your Roster", widget=forms.Textarea)

class RosterIndForm(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ('startDateTime', 'endDateTime', 'role','job', 'oncallTF')
        
    def __init__(self, *args, **kwargs):
        super(RosterIndForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = col_control

class CustomPayCycleForm(forms.Form):
    startDate = forms.DateField(label="starting date")
    finishDate = forms.DateField(label="ending date")
    
    def __init__(self, *args, **kwargs):
        super(CustomPayCycleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = col_control


class DeleteForm(forms.ModelForm):
    class Meta:
        model = OvertimeRow
        fields = ('date',)
        widgets = {"date": forms.HiddenInput()}