# coding: utf-8

from django import forms
from django.forms import ModelForm, Form, TextInput
from django.utils.translation import ugettext as _

from contacts.models import Person, LABORAL_LEVEL_CHOICES, MailTemplate, Excursion, TallerRegistration, Taller
from contacts.widgets import ColumnCheckboxSelectMultiple
from bootstrap_toolkit.widgets import BootstrapTextInput, BootstrapDateInput

from models import STATUS_CHOICES


class PersonCreateForm(ModelForm):
    def __init__(self,*args,**kwrds):
        super(ModelForm,self).__init__(*args,**kwrds)
        for key in self.fields:
            if self.fields[key] and 'class' not in self.fields[key].widget.attrs:
                self.fields[key].widget.attrs['class'] = 'v%s' % self.fields[key].__class__.__name__

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'contact_type')

class PersonUpdateForm(ModelForm):
    def __init__(self,*args,**kwrds):
        super(ModelForm,self).__init__(*args,**kwrds)
        for key in self.fields:
            if self.fields[key] and 'class' not in self.fields[key].widget.attrs:
                self.fields[key].widget.attrs['class'] = 'v%s' % self.fields[key].__class__.__name__

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'nickname','about','photo','id_card',
                  'contact_type','math_society','date_registration','revision','paid','date_paid',
                  'email_address','phone_number','mobile_number','twitter','home_address','home_postalcode','home_town','home_province','location',
                  'laboral_category','laboral_levels','laboral_nrp','laboral_years','laboral_cuerpo','laboral_degree',
                  'laboral_centername','laboral_centercode','laboral_centeraddress','laboral_centerpostalcode','laboral_centertown','laboral_centerprovince',
                  'laboral_centerphone','remarks',)
        widgets = {
        }

class PersonIdentificationForm(ModelForm):
    def __init__(self,*args,**kwrds):
        super(ModelForm,self).__init__(*args,**kwrds)
        self.fields['about'].widget.attrs['rows']  = 3
        self.fields['about'].widget.attrs['cols']  = 75
        self.fields['last_name'].widget.attrs['class']  = 'input-xlarge'
        self.fields['id_card'].widget.attrs['class']  = 'input-small'

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'nickname','about','id_card',)

class PersonRegistrationForm(ModelForm):
    def __init__(self,*args,**kwrds):
        super(ModelForm,self).__init__(*args,**kwrds)
        self.fields['date_registration'].widget.format = '%d/%m/%Y'
        self.fields['date_registration'].input_formats = ['%d/%m/%Y']
        self.fields['date_registration'].widget.attrs['class']  = 'input-small'

        self.fields['date_paid'].widget.format = '%d/%m/%Y'
        self.fields['date_paid'].input_formats = ['%d/%m/%Y']
        self.fields['date_paid'].widget.attrs['class']  = 'input-small'
        self.fields['math_society'].widget.attrs['class']  = 'input-xxlarge'
        self.fields['remarks'].widget.attrs['rows']  = 4
        self.fields['remarks'].widget.attrs['cols']  = 75
        self.fields['remarks'].widget.attrs['class']  = 'input-xxlarge'

        self.fields['paid'].widget = BootstrapTextInput(append='€')
        self.fields['paid'].widget.attrs['class']  = 'input-mini'
        self.fields['lang'].widget.attrs['class']  = 'input-medium'

    class Meta:
        model = Person
        fields = ('contact_type','math_society','date_registration','revision','paid','date_paid','lang','remarks')

class PersonAddressForm(ModelForm):
    def __init__(self,*args,**kwrds):
        super(ModelForm,self).__init__(*args,**kwrds)
        self.fields['phone_number'].widget.attrs['class']  = 'input-small'
        self.fields['mobile_number'].widget.attrs['class']  = 'input-small'
        self.fields['twitter'].widget.attrs['class']  = 'input-medium'
        self.fields['phone_number'].widget.attrs['class']  = 'input-small'
        self.fields['home_postalcode'].widget.attrs['class']  = 'input-mini'
        self.fields['home_address'].widget.attrs['class']  = 'input-xxlarge'


    class Meta:
        model = Person
        fields = ('email_address','phone_number','mobile_number','twitter','home_address','home_postalcode','home_town','home_province',)




class PersonLaboralForm(ModelForm):
    def __init__(self,*args,**kwrds):
        super(ModelForm,self).__init__(*args,**kwrds)
        self.fields['laboral_category'].widget.attrs['class']  = 'input-xxlarge'
        # self.fields['laboral_levels'] = forms.MultipleChoiceField(choices=LABORAL_LEVEL_CHOICES, required=False, widget=forms.CheckboxSelectMultiple())
        self.fields['laboral_cuerpo'].widget.attrs['class']  = 'input-xxlarge'
        self.fields['laboral_degree'].widget.attrs['class']  = 'input-xxlarge'
        self.fields['laboral_centername'].widget.attrs['class']  = 'input-xxlarge'
        self.fields['laboral_centercode'].widget.attrs['class']  = 'input-small'
        self.fields['laboral_centeraddress'].widget.attrs['class']  = 'input-xxlarge'
        self.fields['laboral_centerpostalcode'].widget.attrs['class']  = 'input-mini'
        self.fields['laboral_centerphone'].widget.attrs['class']  = 'input-small'
        self.fields['laboral_years'].widget.attrs['class']  = 'input-mini'

    # laboral_levels = forms.MultipleChoiceField(choices=LABORAL_LEVEL_CHOICES, required=False, widget=ColumnCheckboxSelectMultiple())


    class Meta:
        model = Person
        fields = ('laboral_category','laboral_nrp','laboral_years','laboral_cuerpo','laboral_degree',
                  'laboral_centername','laboral_centercode','laboral_centeraddress','laboral_centerpostalcode','laboral_centertown','laboral_centerprovince',
                  'laboral_centerphone')

class PersonLaboralLevelsForm(Form):
    laboral_levels = forms.MultipleChoiceField(label=_('laboral levels'),choices=LABORAL_LEVEL_CHOICES, required=False, widget=ColumnCheckboxSelectMultiple())


FILTERCONTACT_TYPE_CHOICES = (
    ('', ''),
    ('R', _('Registrant')),
    ('G', _('Guest')),
    ('S', _('Sponsor')),
    ('O', _('Organizer')),
    ('V', _('Volunteer')),
)

FILTERREVISION_CHOICES = (
    ('', ''),
    ('dataok', _('Data ok')),
    ('datanook', _('Incorrect data')),
    ('missdata', _('Missed data')),
    ('unknown', _('Unknown person'))
)

class PersonFilterForm(Form):
    last_name = forms.CharField(label=_('last name'),required = False)
    email_address = forms.CharField(label=_('email address'),required = False)
    contact_type = forms.ChoiceField(label=_('contact type'),required = False, choices = FILTERCONTACT_TYPE_CHOICES )
    id_card = forms.CharField(label=_('ID card'),required = False)
    status = forms.ChoiceField(label=_('status'),required = False, choices =  ( ('', ''),) + STATUS_CHOICES )
    mailnotpaid_unsent = forms.BooleanField(label=_('mail not paid unsent'),required = False)
    mailregister_unsent = forms.BooleanField(label=_('mail registration unsent'),required = False)


class ImportCSVForm(Form):
    fitxer = forms.FileField(label='Fitxer CSV')

class SynchronizeSPIPForm(Form):
    confirma = forms.BooleanField(required=True)

STATS_CHOICES = (
    ('', ''),
    ('contact_type', _('contact type')),
    ('math_society', _('math society')),
    ('province', _('province')),
    ('lang', _('lang')),

)

class StatsForm(Form):
    stats_by = forms.ChoiceField(label=_('stats by'),required = False, choices =  STATS_CHOICES )


class MailTemplateForm(ModelForm):
    def __init__(self,*args,**kwrds):
        super(ModelForm,self).__init__(*args,**kwrds)
        self.fields['body'].widget.attrs['rows']  = 8
        self.fields['body'].widget.attrs['cols']  = 75
        self.fields['body'].widget.attrs['class']  = 'input-xxlarge'
        self.fields['description'].widget.attrs['class']  = 'input-xxlarge'
        self.fields['subject'].widget.attrs['class']  = 'input-xxlarge'
        self.fields['attachment'].widget.attrs['class']  = 'input-large'
        self.fields['attachment2'].widget.attrs['class']  = 'input-large'

    class Meta:
        model = MailTemplate
        fields = ('code','description','subject','body','attachment','attachment2')

class ExcursionFilterForm(Form):
    last_name = forms.CharField(label=_('last name'),required = False)
    email_address = forms.CharField(label=_('email address'),required = False)
    status = forms.ChoiceField(label=_('status'),required = False, choices =  ( ('', ''),) + STATUS_CHOICES )
    mailnotpaid_unsent = forms.BooleanField(label=_('mail not paid unsent'),required = False)
    mailregister_unsent = forms.BooleanField(label=_('mail registration unsent'),required = False)

class ExcursionCreateForm(ModelForm):
    def __init__(self,*args,**kwrds):
        super(ModelForm,self).__init__(*args,**kwrds)
        self.fields['remarks'].widget.attrs['rows']  = 8
        self.fields['remarks'].widget.attrs['cols']  = 50
        self.fields['remarks'].widget.attrs['class']  = 'input-xlarge'
        self.fields['first_name'].widget.attrs['class']  = 'input-large'
        self.fields['last_name'].widget.attrs['class']  = 'input-large'
        self.fields['email_address'].widget.attrs['class']  = 'input-large'
        self.fields['qty_excursion'].widget = forms.Select(choices=  [ (i,i) for i in range(0,8) ])
        self.fields['qty_excursion'].widget.attrs['class']  = 'input-mini'

        self.fields['qty_dinner'].widget = forms.Select(choices=  [ (i,i) for i in range(0,8) ])
        self.fields['qty_dinner'].widget.attrs['class']  = 'input-mini'

        self.fields['qty_vegetarian'].widget = forms.Select(choices=  [ (i,i) for i in range(0,8) ])
        self.fields['qty_vegetarian'].widget.attrs['class']  = 'input-mini'

        self.fields['qty_celiac'].widget = forms.Select(choices=  [ (i,i) for i in range(0,8) ])
        self.fields['qty_celiac'].widget.attrs['class']  = 'input-mini'

        self.fields['alergies'].widget.attrs['class']  = 'input-xxlarge'

        self.fields['qty_bus'].widget = forms.Select(choices=  [ (i,i) for i in range(0,8) ])
        self.fields['qty_bus'].widget.attrs['class']  = 'input-mini'

        self.fields['accommodation_name'].widget.attrs['class']  = 'input-xlarge'
        self.fields['accommodation_address'].widget.attrs['class']  = 'input-xlarge'

    def clean_email_address(self):
        data = self.cleaned_data['email_address']
        person_list = Person.objects.filter(email_address__iexact=data)
        person = None
        if person_list.count() > 0:
            for iter_person in person_list:
                if person is None: person = iter_person
                if iter_person.first_name.lower().strip() == self.cleaned_data['first_name'].lower().strip():
                    person = iter_person
                    break
        else:
            raise forms.ValidationError( _("This email address doesn't exist in the inscription database"))

        try:
            excursion = Excursion.objects.get(person_id__exact=person.id)
            raise forms.ValidationError( _("Your excursion and gala dinner inscriptions already exists. If you want to modify your inscription, please send a message to inscripciones@jaem.es"))
        except Excursion.DoesNotExist:
            pass


        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

    def clean_qty_dinner(self):
        data = self.cleaned_data['qty_dinner']
        qty_excursion = self.cleaned_data['qty_excursion']

        if data == 0 and qty_excursion == 0:
            raise forms.ValidationError( _("You have to select excursion, gala dinner or both"))

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

    def clean_qty_vegetarian(self):
        data = self.cleaned_data['qty_vegetarian']
        try:
            qty_dinner = self.cleaned_data['qty_dinner']
        except:
            return data
        if data > qty_dinner:
            raise forms.ValidationError( _("There are more vegetarian options than dinners selected"))

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

    def clean_qty_celiac(self):
        data = self.cleaned_data['qty_celiac']
        try:
            qty_dinner = self.cleaned_data['qty_dinner']
        except:
            return data

        if data > qty_dinner:
            raise forms.ValidationError( _("There are more celiac options than dinners selected"))

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data


    class Meta:
        model = Excursion
        fields = ('first_name', 'last_name', 'email_address',
                  'qty_excursion','qty_dinner','qty_vegetarian','qty_celiac','alergies',
                  'qty_bus','accommodation_name','accommodation_address','remarks')

class ExcursionUpdateForm(ModelForm):
    def __init__(self,*args,**kwrds):
        super(ModelForm,self).__init__(*args,**kwrds)
        self.fields['remarks'].widget.attrs['rows']  = 8
        self.fields['remarks'].widget.attrs['cols']  = 75
        self.fields['remarks'].widget.attrs['class']  = 'input-xxlarge'
        self.fields['first_name'].widget.attrs['class']  = 'input-large'
        self.fields['last_name'].widget.attrs['class']  = 'input-large'
        self.fields['qty_excursion'].widget = forms.Select(choices=  [ (i,i) for i in range(0,8) ])
        self.fields['qty_excursion'].widget.attrs['class']  = 'input-mini'
        self.fields['qty_dinner'].widget = forms.Select(choices=  [ (i,i) for i in range(0,8) ])
        self.fields['qty_dinner'].widget.attrs['class']  = 'input-mini'
        self.fields['qty_vegetarian'].widget = forms.Select(choices=  [ (i,i) for i in range(0,8) ])
        self.fields['qty_vegetarian'].widget.attrs['class']  = 'input-mini'
        self.fields['qty_celiac'].widget = forms.Select(choices=  [ (i,i) for i in range(0,8) ])
        self.fields['qty_celiac'].widget.attrs['class']  = 'input-mini'
        self.fields['alergies'].widget.attrs['class']  = 'input-xxlarge'
        self.fields['qty_bus'].widget = forms.Select(choices=  [ (i,i) for i in range(0,8) ])
        self.fields['qty_bus'].widget.attrs['class']  = 'input-mini'
        self.fields['accommodation_name'].widget.attrs['class']  = 'input-xlarge'
        self.fields['accommodation_address'].widget.attrs['class']  = 'input-xlarge'

        self.fields['date_registration'].widget.format = '%d/%m/%Y'
        self.fields['date_registration'].input_formats = ['%d/%m/%Y']
        self.fields['date_registration'].widget.attrs['class']  = 'input-small'

        self.fields['date_paid'].widget.format = '%d/%m/%Y'
        self.fields['date_paid'].input_formats = ['%d/%m/%Y']
        self.fields['date_paid'].widget.attrs['class']  = 'input-small'
        self.fields['paid'].widget = BootstrapTextInput(append='€')
        self.fields['paid'].widget.attrs['class']  = 'input-mini'



    class Meta:
        model = Excursion
        fields = ('first_name', 'last_name', 'email_address',
                  'qty_excursion','qty_dinner','qty_vegetarian','qty_celiac','alergies',
                  'qty_bus','accommodation_name','accommodation_address','remarks','date_registration','paid','date_paid')

class TallerRegistrationFilterForm(Form):
    last_name = forms.CharField(label=_('last name'),required = False)
    email_address = forms.CharField(label=_('email address'),required = False)

class TallerRegistrationCreateForm(ModelForm):
    def __init__(self,*args,**kwrds):
        super(ModelForm,self).__init__(*args,**kwrds)
        self.fields['first_name'].widget.attrs['class']  = 'input-large'
        self.fields['last_name'].widget.attrs['class']  = 'input-large'
        self.fields['email_address'].widget.attrs['class']  = 'input-large'
        self.fields['tallers'] = forms.CharField()
        self.fields['tallers'].widget = forms.HiddenInput()
        self.fields['taller'] = forms.ModelChoiceField(queryset=Taller.objects.order_by('day_scheduled', 'time_scheduled'),empty_label='-')
        self.fields['taller'].widget.attrs['class']  = 'input-xxlarge'

    def clean_email_address(self):
        data = self.cleaned_data['email_address']
        person_list = Person.objects.filter(email_address__iexact=data)
        person = None
        if person_list.count() > 0:
            for iter_person in person_list:
                if person is None: person = iter_person
                if iter_person.first_name.lower().strip() == self.cleaned_data['first_name'].lower().strip():
                    person = iter_person
                    break
        else:
            raise forms.ValidationError( _("This email address doesn't exist in the inscription database"))

        # try:
        #     regtaller = TallerRegistration.objects.get(person_id__exact=person.id)
        #     raise forms.ValidationError( _("Your taller registration already exists. If you want to modify your registration, please send a message to inscripciones@jaem.es"))
        # except TallerRegistration.DoesNotExist:
        #     pass

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data


    class Meta:
        model = TallerRegistration
        fields = ('first_name', 'last_name', 'email_address')

class TallerRegistrationUpdateForm(ModelForm):
    def __init__(self,*args,**kwrds):
        super(ModelForm,self).__init__(*args,**kwrds)
        self.fields['remarks'].widget.attrs['rows']  = 8
        self.fields['remarks'].widget.attrs['cols']  = 75
        self.fields['remarks'].widget.attrs['class']  = 'input-xxlarge'
        self.fields['first_name'].widget.attrs['class']  = 'input-large'
        self.fields['last_name'].widget.attrs['class']  = 'input-large'

        self.fields['date_registration'].widget.format = '%d/%m/%Y'
        self.fields['date_registration'].input_formats = ['%d/%m/%Y']
        self.fields['date_registration'].widget.attrs['class']  = 'input-small'


    class Meta:
        model = TallerRegistration
        fields = ('first_name', 'last_name', 'email_address','remarks','date_registration')


