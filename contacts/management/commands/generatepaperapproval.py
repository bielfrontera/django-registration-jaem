# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand, make_option

from django.core.mail import EmailMessage
from django.template.context import Context
from django.template.loader import render_to_string
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

        avui_cat = _date(datetime.now(), "d \d\e F \d\e Y")

        cur_language = translation.get_language()
        try:
            translation.activate('es')
            avui_es = _date(datetime.now(), "d \d\e F \d\e Y")
        except:
            avui_es = avui_cat
        finally:
            translation.activate(cur_language)

        try:
            translation.activate('ca')
            avui_cat = _date(datetime.now(), "d \d\e F \d\e Y")
        finally:
            translation.activate(cur_language)


        print 'Avui cat: ', avui_cat
        print 'Avui es: ', avui_es



        with open('aportacions_acceptades.csv', 'rb') as infile:
            aportacions = csv.DictReader(infile, delimiter=',')
            for aportacio in aportacions:
                lang = '1'
                status = 'pending'
                # Miram si existeix la persona per correu electronic, per cercar si català (2) o castellà (1)
                try:
                    person = Person.objects.get(email_address__iexact=aportacio['email'])
                    lang = person.lang
                    status = person.status
                    print '     >> SI troba registre persona: %s. ' % person.fullname
                except Person.DoesNotExist:
                    print '     << No ha trobat registre persona %s. Assumim castellà ' % aportacio['email']

                tipologia = aportacio['tipologia']
                avui = avui_es
                if tipologia == 'Comunicació':
                    tipologia = 'Comunicación'
                elif tipologia == 'Clip d\'aula':
                    tipologia = 'Clip de aula'

                # Generam la plantilla
                context = {
                    'titol' : aportacio['titol'],
                    'autors' : aportacio['autors'],
                    'tipologia': tipologia,
                    'avui' : avui,
                    'status' : status
                }

                html = render_to_string('contacts/person/certificat_acceptacio_es.pdf.html',context)


                diversos_autors = ( aportacio['autors'].find(';') != -1 )
                if diversos_autors:
                    autor_principal = aportacio['autors'].split(';')[0]
                else:
                    autor_principal = aportacio['autors']

                slug = slugify(autor_principal)
                et_altri = '_et_altri' if diversos_autors else ''
                file_name = 'generated_files/certificats_acceptacio/%s_%s%s.pdf' % ( aportacio['id'] , slug, et_altri)


                result = file(file_name,'wb')

                pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                                         dest=result,
                                                         link_callback=fetch_resources)
                result.close()
                if pdf.err:
                    raise Exception('Error generating pdf. %d errors' % pdf.err )

                print "%s generated" % file_name

def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

