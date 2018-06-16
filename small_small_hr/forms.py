"""
Forms module for small small hr
"""
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import Field, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from phonenumber_field.formfields import PhoneNumberField

from small_small_hr.models import StaffProfile


class StaffProfileAdminForm(forms.ModelForm):
    """
    Form used when managing StaffProfile objects
    """
    first_name = forms.CharField(label=_('First Name'), required=True)
    last_name = forms.CharField(label=_('Last Name'), required=True)
    id_number = forms.CharField(label=_('ID Number'), required=True)
    nhif = forms.CharField(label=_('NHIF'), required=False)
    nssf = forms.CharField(label=_('NSSF'), required=False)
    pin_number = forms.CharField(label=_('PIN Number'), required=False)
    emergency_contact_name = forms.CharField(
        label=_('Emergecy Contact Name'), required=False)
    emergency_contact_number = PhoneNumberField(
        label=_('Emergency Contact Phone Number'), required=False)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Class meta options
        """
        model = StaffProfile
        fields = [
            'first_name',
            'last_name',
            'id_number',
            'phone',
            'sex',
            'role',
            'nhif',
            'nssf',
            'pin_number',
            'address',
            'birthday',
            'leave_days',
            'sick_days',
            'overtime_allowed',
            'start_date',
            'end_date',
            'emergency_contact_name',
            'emergency_contact_number',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'investment-form'
        self.helper.layout = Layout(
            Field('first_name',),
            Field('last_name',),
            Field('phone',),
            Field('id_number',),
            Field('sex',),
            Field('role',),
            Field('nhif',),
            Field('nssf',),
            Field('pin_number',),
            Field('emergency_contact_name',),
            Field('emergency_contact_number',),
            Field('address',),
            Field('birthday',),
            Field('leave_days',),
            Field('sick_days',),
            Field('overtime_allowed',),
            Field('start_date',),
            Field('end_date',),
            Field('emergency_contact_name',),
            Field('emergency_contact_number',),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-primary'),
            )
        )

    def clean_id_number(self):
        """
        Check if id number is unique
        """
        value = self.cleaned_data.get('id_number')
        # pylint: disable=no-member
        if StaffProfile.objects.exclude(
                id=self.instance.id).filter(data__id_number=value).exists():
            raise forms.ValidationError(
                _('This id number is already in use.'))
        return value

    def clean_nssf(self):
        """
        Check if NSSF number is unique
        """
        value = self.cleaned_data.get('nssf')
        # pylint: disable=no-member
        if StaffProfile.objects.exclude(
                id=self.instance.id).filter(data__nssf=value).exists():
            raise forms.ValidationError(
                _('This NSSF number is already in use.'))
        return value

    def clean_nhif(self):
        """
        Check if NHIF number is unique
        """
        value = self.cleaned_data.get('nhif')
        # pylint: disable=no-member
        if StaffProfile.objects.exclude(
                id=self.instance.id).filter(data__nhif=value).exists():
            raise forms.ValidationError(
                _('This NHIF number is already in use.'))
        return value

    def clean_pin_number(self):
        """
        Check if PIN number is unique
        """
        value = self.cleaned_data.get('pin_number')
        # pylint: disable=no-member
        if StaffProfile.objects.exclude(
                id=self.instance.id).filter(data__pin_number=value).exists():
            raise forms.ValidationError(
                _('This PIN number is already in use.'))
        return value

    def save(self, commit=True):  # pylint: disable=unused-argument
        """
        Custom save method
        """
        staffprofile = super().save()

        emergency_phone = self.cleaned_data.get('emergency_contact_number')
        emergency_phone = emergency_phone.as_e164

        json_data = {
            'id_number': self.cleaned_data.get('id_number'),
            'nhif': self.cleaned_data.get('nhif'),
            'nssf': self.cleaned_data.get('nssf'),
            'pin_number': self.cleaned_data.get('pin_number'),
            'emergency_contact_name': self.cleaned_data.get(
                'emergency_contact_name'),
            'emergency_contact_number': emergency_phone,
        }
        staffprofile.data = json_data
        staffprofile.save()

        user = staffprofile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return staffprofile
