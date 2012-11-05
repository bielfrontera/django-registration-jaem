# coding: utf-8

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
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
    
    email_address = models.EmailField(_('email address'), blank=True)     
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
    