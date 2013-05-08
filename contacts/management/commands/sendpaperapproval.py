# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand, make_option

from django.core.mail import EmailMessage
from django.template.context import Context
from django.template.loader import render_to_string
from string import Template
from django.conf import settings
from contacts.models import Person
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.utils import translation
from django.template.defaultfilters import date as _date
from datetime import date, datetime

import StringIO, os, csv
from xhtml2pdf import pisa




class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        print "Enviament comunicacio OK per correu"

        with open('aportacions_acceptades_part3.csv', 'rb') as infile:
            aportacions = csv.DictReader(infile, delimiter=',')
            for aportacio in aportacions:
                lang = '1'
                status = 'pending'
                # Miram si existeix la persona per correu electronic, per cercar si català (2) o castellà (1)
                try:
                    person = Person.objects.get(email_address__iexact=aportacio['email'])
                    lang = person.lang
                    status = person.status
                except Person.DoesNotExist:
                    print '     << No ha trobat registre persona %s.' % aportacio['email']

                tipologia = aportacio['tipologia']
                if tipologia == 'Comunicació':
                    tipologia = 'Comunicación'
                elif tipologia == 'Clip d\'aula':
                    tipologia = 'Clip de aula'

                # Generam la plantilla
                context = {
                    'titol' : aportacio['titol'],
                    'autors' : aportacio['autors'],
                    'tipologia': tipologia,
                    'status' : status
                }




                diversos_autors = ( aportacio['autors'].find(';') != -1 )
                if diversos_autors:
                    autor_principal = aportacio['autors'].split(';')[0]
                else:
                    autor_principal = aportacio['autors']

                slug = slugify(autor_principal)
                et_altri = '_et_altri' if diversos_autors else ''
                base_file_name = '%s_%s%s.pdf' % ( aportacio['id'] , slug, et_altri)
                file_name = 'generated_files/certificats_acceptacio/%s' % base_file_name

                # Enviament per correu del fitxer
                if lang == '1':
                    subject = 'XVI JAEM - Resolución aportación'
                    body = render_to_string('contacts/person/certificat_acceptacio_es_bodymail.html',context)
                else:
                    subject = 'XVI JAEM - Resolució aportació'
                    body = render_to_string('contacts/person/certificat_acceptacio_ca_bodymail.html',context)

                email = EmailMessage(subject, body, settings.EMAIL_FROM, [aportacio['email']])
                email.attach_file(file_name)

                try:
                    email.send()
                    print 'Mail sent to %s ' % aportacio['email']
                except Exception as inst:
                    status = 'Error sending to %s. Tipus: %s . Missatge: %s' % (aportacio['email'], type(inst) , inst)
                except:
                    status = 'Error sending mail to %s' % aportacio['email']




