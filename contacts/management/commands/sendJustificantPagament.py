# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand, make_option

from django.template.context import Context
from django.conf import settings
from contacts.models import Person
from django.utils import translation
from django.template.defaultfilters import date as _date
from datetime import date, datetime
from contacts.functions.mailtemplate import sendTemplateMail
from django.utils.translation import ugettext as _





class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        print "Enviament confirmacio inscripcio ok"

        person_list = Person.objects.all()
        person_list = person_list.filter(date_mailregister__isnull = True, status='ok_all')[:5]

        for person in person_list:
            print person.fullname
            avui = _date(datetime.now(), "d \d\e F \d\e Y")

            if person.lang == '1':
                cur_language = translation.get_language()
                try:
                    translation.activate('es')
                    avui = _date(datetime.now(), "d \d\e F \d\e Y")
                finally:
                    translation.activate(cur_language)

            kwvars = {
                'object': person,
                'avui': avui
            }
            # ('R', _('Registrant')) -> justpagament
            # else (convidat, organitzacio, etc) -> justregistre
            if person.contact_type == 'R':
                if person.lang == '2':
                    mailtemplate = 'justpagament_cat'
                else:
                    mailtemplate = 'justpagament_esp'
            else:
                if person.lang == '2':
                    mailtemplate = 'justregistre_cat'
                else:
                    mailtemplate = 'justregistre_esp'

            context = Context(kwvars)
            status = sendTemplateMail(context,mailtemplate,[person.email_address])
            if status == _('Mail sent'):
                person.date_mailregister = datetime.now()
                person.save()
                print "Mail sended to %s" % person.email_address


