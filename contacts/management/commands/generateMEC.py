from django.core.management.base import NoArgsCommand, make_option

from django.core.mail import EmailMessage
from django.template.context import Context
from django.template.loader import render_to_string
from django.conf import settings
from contacts.models import Person
from django.utils.translation import ugettext as _


import StringIO, os
from xhtml2pdf import pisa




class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def fetch_resources(uri, rel):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        return path


    def handle_noargs(self, **options):
        print "Testing"
        person_list = Person.objects.all()
        person_list = person_list.filter(last_name__istartswith='Frontera')

        for person in person_list:
            context = {
                'object' : person
            }
            html = render_to_string('contacts/person/ficha_participantes_mec2.html',context)
            result = file('ficha_participantes_%s.pdf' % person.slug,'wb')

            pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                                    dest=result,
                                                    link_callback=self.fetch_resources)
            result.close()
            print "ficha_participantes_%s.pdf generated" % person.slug
            if pdf.err:
                raise Exception('Error generating pdf. %d errors' % pdf.err )
