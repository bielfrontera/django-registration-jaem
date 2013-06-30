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

    help = "generateCertificatAportacio"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        print "Generacio certificats aportacio"

        with open('../programa/input/clipsaula.csv', 'rb') as infile:
            aportacions = csv.DictReader(infile, delimiter=',')
            for aportacio in aportacions:
                lang = '1'
                # Miram si existeix la persona per correu electronic, per cercar si català (2) o castellà (1)
                person_list = Person.objects.filter(email_address__iexact=aportacio['Correu electrònic'])
                if person_list.count() > 0:
                    person = None
                    for iter_person in person_list:
                        if person is None: person = iter_person
                        if iter_person.first_name in aportacio['Autors'].decode('utf-8') and iter_person.last_name in aportacio['Autors'].decode('utf-8'):
                            person = iter_person
                            print '     >> TROBA: %s. ' % person.fullname
                            break

                    lang = person.lang
                    print '     >> SI troba registre persona: %s. ' % person.fullname
                else:
                    print '     << No ha trobat registre persona %s. Assumim castellà ' % aportacio['Correu electrònic']

                tipologia = aportacio['Tipologia']
                if lang == '1':
                    if tipologia == 'Comunicación':
                        tipologia = 'la comunicación'
                    elif tipologia == 'Ponencia':
                        tipologia = 'la ponencia'
                    elif tipologia == 'Taller':
                        tipologia = 'el taller'
                    elif tipologia == 'Plenaria':
                        tipologia = 'la plenaria'
                    elif tipologia == 'Zoco':
                        tipologia = 'ha presentado el zoco'
                    elif tipologia == 'Clip d\'aula':
                        tipologia = 'ha presentado el clip de aula'
                else:
                    if tipologia == 'Comunicación':
                        tipologia = 'la comunicació'
                    elif tipologia == 'Ponencia':
                        tipologia = 'la ponència'
                    elif tipologia == 'Taller':
                        tipologia = 'el taller'
                    elif tipologia == 'Plenaria':
                        tipologia = 'la plenària'
                    elif tipologia == 'Zoco':
                        tipologia = 'ha presentat el zoco'
                    elif tipologia == 'Clip d\'aula':
                        tipologia = 'ha presentat el clip d\'aula'

                # Generam la plantilla
                context = {
                    'titol' : aportacio['Títol'],
                    'autors' : aportacio['Autors'],
                    'tipologia': tipologia
                    }

                template = 'contacts/person/certificat_aportacio_es.pdf.html' if lang != '2' else 'contacts/person/certificat_aportacio_ca.pdf.html'

                filename_base = "%s %s %s %s %s %s" % (aportacio['Edifici'].decode('utf-8'), aportacio['Aula'].decode('utf-8'),aportacio['Dia'].decode('utf-8'),aportacio['Hora'].decode('utf-8'),aportacio['Tipologia'].decode('utf-8'),aportacio['Títol'].decode('utf-8')[0:15])
                filename_base = slugify(filename_base)

                for autor in aportacio['Autors'].split(';'):
                    aux_autor = autor.split(',')
                    context['autor'] = aux_autor[1] + ' ' + aux_autor[0]
                    html = render_to_string(template,context)
                    filename = 'generated_files/certificat_aportacio/%s__%s.pdf' % (filename_base, slugify(autor))
                    result = file(filename,'wb')
                    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                                         dest=result,
                                                         link_callback=fetch_resources)
                    result.close()
                    if pdf.err:
                        raise Exception('Error generating pdf. %d errors' % pdf.err )


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

