from django.core.management.base import NoArgsCommand, make_option

from django.core.mail import EmailMessage
from django.template.context import Context
from django.template.loader import render_to_string
from django.conf import settings
from contacts.models import Person
from django.utils.translation import ugettext as _
from django.template.defaultfilters import date as _date
from datetime import date, datetime
from django.utils import translation
from django.template.defaultfilters import slugify


import StringIO, os
from xhtml2pdf import pisa




class Command(NoArgsCommand):

    help = ""

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )


    def handle_noargs(self, **options):
        person_list = Person.objects.all()
        person_list = person_list.exclude(status='cancelled')
        person_list = person_list.exclude(contact_type='V')



        for person in person_list:
            context = {
                'object' : person
            }
            template = 'contacts/person/certificat_assistencia_es.pdf.html' if person.lang != '2' else 'contacts/person/certificat_assistencia_ca.pdf.html'
            html = render_to_string(template,context)
            filename = 'generated_files/certificat_assistencia/%s.pdf' % slugify("%s %s" % (person.last_name, person.first_name))
            result = file(filename,'wb')

            pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                                    dest=result,
                                                    link_callback=fetch_resources)
            result.close()
            print filename
            if pdf.err:
                raise Exception('Error generating pdf. %d errors' % pdf.err )


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path