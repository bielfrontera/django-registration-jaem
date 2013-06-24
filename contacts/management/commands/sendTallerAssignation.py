# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand, make_option

from django.template.context import Context
from django.conf import settings
from contacts.models import TallerRegistration
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

        regtaller_list = TallerRegistration.objects.all()
        regtaller_list = regtaller_list.filter(date_mailassignation__isnull = True)[:25]

        for regtaller in regtaller_list:
            kwvars = {
                'object': regtaller
            }
            mailtemplate = 'tll_assignation_es' if regtaller.person.lang != '2' else 'tll_assignation_ca'
            context = Context(kwvars)
            status = sendTemplateMail(context,mailtemplate,[regtaller.email_address])
            if status == _('Mail sent'):
                regtaller.date_mailassignation = datetime.now()
                regtaller.save()
                print "Mail sended to %s" % regtaller.email_address
            else:
                print "Error ocurred sendint to %s. Error message: %s" % (regtaller.email_address, status )


