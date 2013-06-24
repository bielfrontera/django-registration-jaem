# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand, make_option

from django.template.context import Context
from django.conf import settings
from contacts.models import Taller, TallerRelation, TallerRegistration
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Command(NoArgsCommand):

    help = ""

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        print "Sorteig (després d'haver fet l'assignació de tallers amb places suficients)"
        count_assigned = 0
        registration_list = TallerRegistration.objects.filter(date_mailassignation__isnull = True).order_by('?')
        for regtaller in registration_list:
            print "    Persona %s" % (regtaller.fullname)
            for registration in regtaller.tallers_ordered:
                if not registration.assigned:
                    if registration.has_preferenced_assigned:
                        if not registration.discarted:
                            registration.assigned = False
                            registration.discarted = True
                            registration.save()
                            print "       ---- Descarta %s " % registration.taller
                    else:
                        if not registration.taller.full:
                            # Hi ha places disponibles per aquest taller. L'assignam, i sortim.
                            count_assigned = count_assigned +1
                            registration.assigned = True
                            registration.discarted = False
                            registration.save()
                            # Discard all registrations of this range
                            registration.discard_others()
                            print "                 +++++ Selecciona %s " % registration.taller
                            if registration.taller.max_attendants == registration.taller.num_attendants:
                                registration.taller.full = True
                                registration.taller.save()
                                print "    ***** Taller ple"
                            break


        print "Final: S'han assignat un total de %d tallers" % count_assigned


