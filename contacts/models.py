# coding: utf-8

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.generic import GenericRelation
from django.conf import settings

from contacts.geolocation import LocationField

from datetime import date
import time
import ast



CONTACT_TYPE_CHOICES = (
    ('R', _('Registrant')),
    ('G', _('Guest')),
    ('S', _('Sponsor')),
    ('O', _('Organizer')),
    ('V', _('Volunteer')),
)


LABORAL_CATEGORY_CHOICES = (
    ('0', 'Sense especificar'),
    ('1', 'Funcionario/a ME o CCAA'),
    ('2', 'Interino/a ME o CCAA'),
    ('3', 'Otros funcionarios (Universidades)'),
    ('4', 'Profesor/a Privada concertada'),
    ('5', 'Profesor/a Privada no concertada'),
    ('6', 'Sin experiencia docente (Magisterio/Formación inic...'),
)

LABORAL_LEVEL_CHOICES = (
    (1, 'Educación Infantil'),
    (2, 'Educación Primaria'),
    (3, 'Enseñanza Secundaria Obligatoria'),
    (4, 'Bachillerato'),
    (5, 'Formación Profesional'),
    (7, 'Enseñanzas Artísticas y de Idiomas'),
    (8,'Escuelas Oficiales de Idiomas'),
    (9,'Educación Especial '),
    (10,'Educación Permanente de  adultos'),
    (11,'Equipos Orientación Educación y Psicopedagógica '),
    (12,'Profesores de nacionalidad extranjera'),
    (13,'Personal de otros ámbitos: (Inspectores al Servicio de la Admón. Educativa, ...) '),
    (6,'Universidad'),
)

LABORAL_CUERPO_CHOICES = (
    ('0', 'Sense especificar'),
    ('1', 'Maestros'),
    ('2', 'Prof. Ens. Secundaria'),
    ('3', 'Prof. Técnicos de Form. Profes.'),
    ('4', 'Prof. de Esc. Of. De Idiomas'),
    ('5', 'Prof. de Música y Artes Esc.'),
    ('6', 'Catedr. de Música y Artes Esc.'),
    ('7', 'Maestros de taller Artes Plást. y Diseño'),
    ('8', 'Prof. de  Artes Plást. y Diseño'),
    ('9', 'Inspectores de Educación: ME o CCAA'),
    ('10', 'Catedráticos'),
    ('11', 'Prof. Universitarios.'),
)

MATH_SOCIETY_CHOICES = (
    ('1', 'Ninguna'),
    ('2', 'FEEMCAT - Federació d’Entitats per l’Ensenyament de les Matemátiques a Catalunya'),
    ('3', 'Organización Española para La Coeducación Matemática «Ada Byron»'),
    ('4', 'Sociedad Andaluza de Educación Matemática «Thales»'),
    ('5', 'Sociedad Aragonesa de Profesores de Matemáticas «Pedro Sánchez Ciruelo»'),
    ('6', 'Sociedad Asturiana de Educación Matemática «Agustín de Pedrayes»'),
    ('7', 'Sociedad Canaria de Profesores de Matemáticas «Isaac Newton»'),
    ('8', 'Asociación Castellana y Leonesa de Educación Matemática «Miguel de Guzmán»'),
    ('9', 'Sociedad dos Ensinantes de Ciencia de Galicia (ENCIGA)'),
    ('10', 'Sociedad Extremeña de Educación Matemática «Ventura Reyes Prósper»'),
    ('11', 'Sociedad Madrileña de Profesores de Matemáticas «Emma Castelnuovo»'),
    ('12', 'Sociedad Matemática de Profesores de Cantabria'),
    ('13', 'Matematika lraskasicen Nafar Elkartea Tornamira'),
    ('14', 'Sociedad «Puiq Adam» de Profesores de Matemáticas'),
    ('15', 'Societat d’Educaciò Matemática de la Comunitat Valenciana «Al-Khwarizmi»'),
    ('16', 'Sociedad Castellano Manchega de Profesores de Matemáticas (SCMPM)'),
    ('17', 'Sociedad de Educación Matemática de la región de Murcia (SEMRM)'),
    ('18', 'Sociedad Riojana de Profesores de matemáticas «A Prima»'),
    ('19', 'Asociacion Galega de Profesores de Educación Matemática (AGAPEMA)'),
    ('20', 'Sociedad Melillense de Educación Matemática'),
    ('21', 'SBM – XEIX Societat Balear de Matemàtiques'),
)
MATH_SOCIETY_CHOICES_MINI = {
    '1':'Cap',
    '2':'FEEMCAT',
    '3':'Ada Byron',
    '4':'SAEM-Thales',
    '5':'Aragonesa',
    '6':'Asturiana',
    '7':'Canaria',
    '8':'CyL',
    '9':'ENCIGA',
    '10':'Extremadura',
    '11':'Madrid',
    '12':'Cantabria',
    '13':'Navarra',
    '14':'Puig Adam',
    '15':'Valenciana',
    '16':'Manchega',
    '17':'Murcia',
    '18':'Riojana',
    '19':'AGAPEMA',
    '20':'Melillense',
    '21':'SBM-XEIX',
}


REVISION_CHOICES = (
    ('dataok', _('Data ok')),
    ('datanook', _('Incorrect data')),
    ('missdata', _('Missed data')),
    ('pendent', _('Pendent'))
)

STATUS_CHOICES = (
    ('pendent', 'Pendent'),
    ('ok_notpaid', 'Revisat / No pagat'),
    ('notpaid_late', 'Pagament retrassat'),
    ('nook_paid', 'No revisat / Pagat'),
    ('ok_all', 'Inscripció ok'),
    ('cancelled', 'Inscripció anul·lada'),
)


LANG_CHOICES = (
    ('1', 'Castellà'),
    ('2', 'Català')
)

class Person(models.Model):
    """Person model."""
    # DADES PERSONALS
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=200)
    nickname = models.CharField(_('nickname'), max_length=100, blank=True)
    slug = models.SlugField(_('slug'), max_length=50, unique=True)
    about = models.TextField(_('about'), blank=True)
    photo = models.ImageField(_('photo'), upload_to='contacts/person/', blank=True)
    contact_type = models.CharField(_('contact type'), max_length=1,
        choices=CONTACT_TYPE_CHOICES, default='R', blank=True)
    id_card = models.CharField(_('ID card'), max_length=20, null=True,blank=True)

    # DIRECCIO - CASA
    home_address = models.CharField(_('address'), max_length=200, blank=True)
    home_postalcode = models.CharField(_('postal code'), max_length=10, blank=True)
    home_town = models.CharField(_('town'), max_length=200, null=True, blank=True)
    home_province = models.CharField(_('province'), max_length=200, blank=True)

    email_address = models.EmailField(_('email address'), db_index=True, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=50, blank=True)
    mobile_number = models.CharField(_('mobile number'), max_length=50, blank=True)
    twitter = models.CharField(_('twitter'), max_length=22, null=True,blank=True)

    # DADES PROFESSIONALS
    laboral_category = models.CharField(_('laboral category'), max_length=1,
        choices=LABORAL_CATEGORY_CHOICES, default='0', blank=True)
    #laboral_levels = models.CommaSeparatedIntegerField(_('laboral levels'), max_length=100,
    #    choices=LABORAL_LEVEL_CHOICES, blank=True)
    laboral_levels = models.CharField(_('laboral levels'), max_length=100,null=True,blank=True)
    laboral_nrp = models.CharField(_('NRP'), max_length=30, null=True,blank=True)
    laboral_years = models.IntegerField(_('years experience'),null=True, blank=True)
    laboral_cuerpo = models.CharField(_('cos docent'),max_length=2,
        choices=LABORAL_CUERPO_CHOICES, default='0', blank=True)
    laboral_degree = models.CharField(_('degree'), max_length=200, null=True,blank=True)


    # CENTRE DE FEINA
    laboral_centername = models.CharField(_('center name'), max_length=200, null=True,blank=True)
    laboral_centercode = models.CharField(_('center code'), max_length=20, null=True,blank=True)
    laboral_centeraddress = models.CharField(_('address'), max_length=200, blank=True)
    laboral_centerpostalcode = models.CharField(_('postal code'), max_length=10, blank=True)
    laboral_centertown = models.CharField(_('town'), max_length=200, null=True, blank=True)
    laboral_centerprovince = models.CharField(_('province'), max_length=200, blank=True)
    laboral_centerphone = models.CharField(_('phone number'), max_length=50, blank=True)

    # SOCIETAT FEDERADA
    math_society = models.CharField(_('math society'),max_length=2,
        choices=MATH_SOCIETY_CHOICES, default='1', blank=True)


    remarks =  models.TextField(_('remarks'), null=True,blank=True)
    lang = models.CharField(_('lang'), max_length=1,choices=LANG_CHOICES, default='1', blank=True)
    external_id = models.IntegerField(_('external id'),db_index=True,null=True,blank=True)


    # location = LocationField(_('location'), max_length=50, blank=True, null=True)
    location = models.CharField(_('location'), max_length=50, blank=True, null=True)

    # Revisio
    date_registration = models.DateTimeField(_('date registration'),null=True, blank=True)
    revision = models.CharField(_('revision'), max_length=8,choices=REVISION_CHOICES, default='pendent', blank=True)
    status = models.CharField(_('status'), max_length=15,choices=STATUS_CHOICES, default='pendent', blank=True)
    paid = models.DecimalField(_('paid'),max_digits=5, decimal_places=2,null=True,blank=True)
    date_paid = models.DateTimeField(_('date paid'),null=True, blank=True)
    date_mailnotpaid = models.DateTimeField(_('date mail not paid'),null=True, blank=True)
    date_mailregister= models.DateTimeField(_('date mail registration'),null=True, blank=True)

    user = models.OneToOneField(User, blank=True, null=True)

    note = GenericRelation(Comment, object_id_field='object_pk')

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    user_add = models.ForeignKey(User, blank=True, null=True, related_name='contact-add')

    date_modified = models.DateTimeField(_('date modified'), auto_now=True)
    user_modify = models.ForeignKey(User, blank=True, null=True, related_name='contact-modified')


    class Meta:
        db_table = 'contacts_people'
        ordering = ('last_name', 'first_name')
        verbose_name = _('person')
        verbose_name_plural = _('people')

    def __unicode__(self):
        return self.fullname

    @property
    def fullname(self):
        return u"%s %s" % (self.first_name, self.last_name)

    @property
    def get_laboral_levels(self):
        r_str = self.laboral_levels
        try:
            levels = ast.literal_eval(self.laboral_levels)
            levels_int = [int(level) for level in levels]
            levels_labels = [dict(LABORAL_LEVEL_CHOICES)[level] for level in levels_int]
            r_str = " / ".join(levels_labels)
        except:
            pass
        return r_str

    @property
    def get_label(self):
        label = ''
        if self.status == 'ok_notpaid':
            label = 'warning'
        elif self.status == 'notpaid_late':
            label = 'important'
        elif self.status == 'nook_paid':
            label = 'info'
        elif self.status == 'ok_all':
            label = 'success'
        elif self.status == 'cancelled':
            label = 'inverse'
        return label

    @property
    def get_math_society_display_mini(self):
        # MATH_SOCIETY_CHOICES_MINI
        return MATH_SOCIETY_CHOICES_MINI[self.math_society]


    @permalink
    def get_absolute_url(self):
        return ('contacts_person_detail', None, {
            'slug': self.slug,
        })

    @permalink
    def get_update_url(self):
        return ('contacts_person_update', None, {
            'slug': self.slug,
        })

    @permalink
    def get_delete_url(self):
        return ('contacts_person_delete', None, {
            'slug': self.slug,
        })
    @permalink
    def get_cancel_url(self):
        return ('contacts_person_cancel', None, {
            'slug': self.slug,
        })


    @permalink
    def get_justificantpagament_url(self):
        return ('contacts_person_justificantpagament', None, {
            'slug': self.slug,
        })

    @permalink
    def get_justificantregistre_url(self):
        return ('contacts_person_justificantregistre', None, {
            'slug': self.slug,
        })

    @permalink
    def get_mail_url(self):
        return ('contacts_person_mail', None, {
            'slug': self.slug,
            'code': None
        })

    @permalink
    def get_mailjustificantpagament_url(self):
        return ('contacts_person_mailjustificantpagament', None, {
            'slug': self.slug,
        })

    @permalink
    def get_mailpagamentretrasat_url(self):
        return ('contacts_person_mailpagamentretrasat', None, {
            'slug': self.slug,
        })

    @permalink
    def get_mailhistory_url(self):
        return ('contacts_person_mailhistory', None, {
            'id': self.id,
        })



class MailTemplate(models.Model):
    code = models.CharField(_('code'), max_length=20, unique=True)
    subject = models.CharField(_('subject'), max_length=200)
    description = models.CharField(_('description'), max_length=250, blank=True)
    body = models.TextField(_('body'), blank=True)
    attachment = models.CharField(_('attachment'), max_length=200, blank=True)
    attachment2 = models.CharField(_('second attachment'), max_length=200, blank=True)

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    user_add = models.ForeignKey(User, blank=True, null=True, related_name='add')
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)
    user_modify = models.ForeignKey(User, blank=True, null=True, related_name='modified')

    class Meta:
        db_table = 'contacts_mailtemplate'
        verbose_name = _('Mail template')
        verbose_name_plural = _('Mail templates')

    def __unicode__(self):
        return  u"%s - %s" % (self.code, self.subject)


    @permalink
    def get_absolute_url(self):
        return ('contacts_mailtemplate_detail', None, {
            'code': self.code,
        })

    @permalink
    def get_update_url(self):
        return ('contacts_mailtemplate_update', None, {
            'code': self.code,
        })

    @permalink
    def get_delete_url(self):
        return ('contacts_mailtemplate_delete', None, {
            'code': self.code,
        })

    @permalink
    def get_copy_url(self):
        return ('contacts_mailtemplate_copy', None, {
            'code': self.code,
        })


LABORAL_CATEGORY_CHOICES = (
    ('0', 'Sense especificar'),
    ('1', 'Funcionario/a ME o CCAA'),
    ('2', 'Interino/a ME o CCAA'),
    ('3', 'Otros funcionarios (Universidades)'),
    ('4', 'Profesor/a Privada concertada'),
    ('5', 'Profesor/a Privada no concertada'),
    ('6', 'Sin experiencia docente (Magisterio/Formación inic...'),
)

class Excursion(models.Model):
    # DADES PERSONALS
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=200)
    email_address = models.EmailField(_('email address'), db_index=True, blank=True)
    qty_excursion = models.IntegerField(_('excursion qty'),null=True, blank=True)
    qty_dinner = models.IntegerField(_('dinner qty'),null=True, blank=True)
    qty_vegetarian = models.IntegerField(_('vegetarian qty'),null=True, blank=True)
    qty_celiac = models.IntegerField(_('celiac qty'),null=True, blank=True)
    alergies = models.CharField(_('alergies'), max_length=200, blank=True)
    qty_bus = models.IntegerField(_('bus qty'),null=True, blank=True)
    accommodation_name = models.CharField(_('accommodation name'), max_length=200, blank=True)
    accommodation_address = models.CharField(_('accommodation address'), max_length=200, blank=True)

    remarks =  models.TextField(_('remarks'), null=True,blank=True)

    # Revisio
    date_registration = models.DateTimeField(_('date registration'),null=True, blank=True)
    status = models.CharField(_('status'), max_length=15,choices=STATUS_CHOICES, default='pendent', blank=True)
    paid = models.DecimalField(_('paid'),max_digits=5, decimal_places=2,null=True,blank=True)
    date_paid = models.DateTimeField(_('date paid'),null=True, blank=True)
    date_mailnotpaid = models.DateTimeField(_('date mail not paid'),null=True, blank=True)
    date_mailregister= models.DateTimeField(_('date mail registration'),null=True, blank=True)

    person = models.OneToOneField(Person, blank=True, null=True)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    user_add = models.ForeignKey(User, blank=True, null=True, related_name='excursion-add')
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)
    user_modify = models.ForeignKey(User, blank=True, null=True, related_name='excursion-modified')

    class Meta:
        db_table = 'contacts_excursion'
        verbose_name = _('Excursion and Dinner registration')
        verbose_name_plural = _('Excursion and Dinner registrations')

    def __unicode__(self):
        return  u"%s" % (self.fullname)


    @property
    def fullname(self):
        return u"%s %s" % (self.first_name, self.last_name)

    @property
    def price(self):
        dinner = self.qty_dinner
        excursion = self.qty_excursion
        bus = self.qty_bus

        if self.person and self.person.contact_type in ['O','G']:
            if dinner > 0:
                dinner = dinner - 1
            if excursion > 0:
                excursion = excursion - 1
            if bus > 0:
                bus = bus - 1

        return dinner * 47 + excursion * 5 + bus * 5


    @property
    def get_label(self):
        label = ''
        if self.status == 'ok_notpaid':
            label = 'warning'
        elif self.status == 'notpaid_late':
            label = 'important'
        elif self.status == 'nook_paid':
            label = 'info'
        elif self.status == 'ok_all':
            label = 'success'
        elif self.status == 'cancelled':
            label = 'inverse'
        return label


    @permalink
    def get_absolute_url(self):
        return ('contacts_excursion_detail', None, {
            'id': self.id,
        })

    @permalink
    def get_update_url(self):
        return ('contacts_excursion_update', None, {
            'id': self.id,
        })

    @permalink
    def get_delete_url(self):
        return ('contacts_excursion_delete', None, {
            'id': self.id,
        })

    @permalink
    def get_cancel_url(self):
        return ('contacts_excursion_cancel', None, {
            'id': self.id,
        })

    @permalink
    def get_justificantpagament_url(self):
        return ('contacts_excursion_justificantpagament', None, {
            'id': self.id,
        })

    @permalink
    def get_mail_url(self):
        return ('contacts_excursion_mail', None, {
            'id': self.id,
            'code': None
        })

    @permalink
    def get_mailjustificantpagament_url(self):
        return ('contacts_excursion_mailjustificantpagament', None, {
            'id': self.id,
        })

    @permalink
    def get_mailpagamentretrasat_url(self):
        return ('contacts_excursion_mailpagamentretrasat', None, {
            'id': self.id,
        })

class Taller(models.Model):
    title = models.CharField(_('title'), max_length=200)
    authors = models.CharField(_('authors'), max_length=250)
    day_scheduled = models.IntegerField(_('day'),null=True, blank=True)
    time_scheduled = models.CharField(_('time'), max_length=20)
    building = models.CharField(_('building'), max_length=20)
    room = models.CharField(_('room'), max_length=20)
    max_attendants = models.IntegerField(_('max attendants'),null=True, blank=True)
    full = models.BooleanField(default=False)

    class Meta:
        db_table = 'contacts_taller'
        verbose_name = _('Taller')
        verbose_name_plural = _('Tallers')

    def __unicode__(self):
        return  u"Dia %s %s: %s" % (self.day_scheduled, self.time_scheduled, self.title)

    @property
    def num_attendants(self):
        return self.tallerrelation_set.filter(assigned=True).count()

    @property
    def attendants(self):
        return self.tallerrelation_set.filter(assigned=True)

    @property
    def num_registrations(self):
        return self.taller_registrations.all().count()


    @property
    def registrations(self):
        return self.taller_registrations.all()

    @property
    def num_discarted(self):
        return self.tallerrelation_set.filter(discarted=True).count()


class TallerRegistration(models.Model):
    # DADES PERSONALS
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=200)
    email_address = models.EmailField(_('email address'), db_index=True, blank=True)
    tallers = models.ManyToManyField(Taller,related_name='taller_registrations',through='TallerRelation')
    password = models.CharField(_('password'), max_length=20)
    remarks =  models.TextField(_('remarks'), null=True,blank=True)
    # Revisio
    date_registration = models.DateTimeField(_('date registration'),null=True, blank=True)
    date_mailassignation= models.DateTimeField(_('date mail assignation'),null=True, blank=True)

    person = models.OneToOneField(Person, blank=True, null=True)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    user_add = models.ForeignKey(User, blank=True, null=True, related_name='regtaller-add')
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)
    user_modify = models.ForeignKey(User, blank=True, null=True, related_name='regtaller-modified')

    class Meta:
        db_table = 'contacts_regtaller'
        verbose_name = _('Taller registration')
        verbose_name_plural = _('Tallers registrations')

    def __unicode__(self):
        return  u"%s" % (self.fullname)


    @property
    def fullname(self):
        return u"%s %s" % (self.first_name, self.last_name)

    @property
    def num_tallers_assigned(self):
        return self.tallerrelation_set.filter(assigned=True).count()

    @property
    def tallers_assigned(self):
        return self.tallerrelation_set.filter(assigned=True)

    @property
    def num_tallers_discarted(self):
        return self.tallerrelation_set.filter(discarted=True).count()


    @property
    def tallers_ordered(self):
        return self.tallerrelation_set.order_by('preference_order')


    @property
    def num_tallers(self):
        return self.tallers.count()


    @permalink
    def get_absolute_url(self):
        return ('contacts_regtaller_detail', None, {
            'id': self.id,
        })

    @permalink
    def get_update_url(self):
        return ('contacts_regtaller_update', None, {
            'id': self.id,
        })

    @permalink
    def get_delete_url(self):
        return ('contacts_regtaller_delete', None, {
            'id': self.id,
        })

    @permalink
    def get_cancel_url(self):
        return ('contacts_regtaller_cancel', None, {
            'id': self.id,
        })

class TallerRelation(models.Model):
    taller_registration = models.ForeignKey(TallerRegistration)
    taller = models.ForeignKey(Taller)
    preference_order = models.IntegerField(_('preference order'),null=True, blank=True, default=100)
    assigned = models.BooleanField(default=False)
    discarted = models.BooleanField(default=False)

    def has_preference_with(self,taller_relation):
        if self.taller.day_scheduled != taller_relation.taller.day_scheduled:
            return None

        if self.taller.time_scheduled != taller_relation.taller.time_scheduled:
            return None

        if self.preference_order < taller_relation.preference_order:
            return True
        else:
            return False

    @property
    def has_preferenced_assigned(self):
        has_preferenced = False
        for other_taller_relation in self.taller_registration.tallerrelation_set.all():
            if other_taller_relation.id != self.id and other_taller_relation.assigned:
                result = self.has_preference_with(other_taller_relation)
                if result is None:
                    continue

                if not result:
                    has_preferenced = True
                    break

        return has_preferenced

    def discard_others(self):
        for other_taller_relation in self.taller_registration.tallerrelation_set.all():
            if not other_taller_relation.discarted:
                result = self.has_preference_with(other_taller_relation)
                if result is None:
                    continue
                if result:
                    other_taller_relation.assigned = False
                    other_taller_relation.discarted = True
                    other_taller_relation.save()


