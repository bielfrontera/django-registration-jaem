# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand, make_option

from django.template.context import Context
from django.conf import settings
from contacts.models import Person, Excursion
from django.utils import translation
from django.template.defaultfilters import date as _date
from datetime import date, datetime
from contacts.functions.mailtemplate import sendTemplateMail
from django.utils.translation import ugettext as _





class Command(NoArgsCommand):

    help = ""

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        print "Enviament confirmacio inscripcio sopar ok"

        excursion_list = Excursion.objects.all()
        excursion_list = excursion_list.filter(date_mailregister__isnull = True, status='ok_all')[:5]

        for excursion in excursion_list:
            print excursion.fullname
            person = excursion.person
            avui = _date(datetime.now(), "d \d\e F \d\e Y")
            cur_language = translation.get_language()

            try:
                if person.lang == '2':
                    translation.activate('ca')
                    avui = _date(datetime.now(), "d \d\e F \d\e Y")
                else:
                    translation.activate('es')
                    avui = _date(datetime.now(), "d \d\e F \d\e Y")
            finally:
                translation.activate(cur_language)

            kwvars = {
                'object': excursion,
                'avui': avui
            }
            # ('R', _('Registrant')) -> justpagament
            # else (convidat, organitzacio, etc) -> justregistre
            if person.lang == '2':
                mailtemplate = 'exc_justpagament_cat'
            else:
                mailtemplate = 'exc_justpagament_esp'

            context = Context(kwvars)
            status = sendTemplateMail(context,mailtemplate,[excursion.email_address])
            if status == _('Mail sent'):
                excursion.date_mailregister = datetime.now()
                excursion.save()
                print "Mail sended to %s" % excursion.email_address
            else:
                print "Error ocurred sendint to %s. Error message: %s" % (excursion.email_address, status )


