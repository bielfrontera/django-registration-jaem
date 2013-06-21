# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand, make_option

from django.template.context import Context
from django.conf import settings
from contacts.models import Taller, TallerRelation, TallerRegistration


class Command(NoArgsCommand):

    help = ""

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        print "Assignació de tots els tallers que no han superat places maximes"
        count_assigned = 0
        taller_list = Taller.objects.all()
        for taller in taller_list:
            if taller.max_attendants >= taller.num_registrations - taller.num_discarted:
                print "    Taller %s-%s" % (taller.id, taller.title)
                for registration in taller.tallerrelation_set.all():
                    if not registration.assigned:
                        if registration.has_preferenced_assigned:
                            registration.assigned = False
                            registration.discarted = True
                            registration.save()
                        else:
                            count_assigned = count_assigned +1
                            registration.assigned = True
                            registration.discarted = False
                            registration.save()
                            # Discart all registrations of their range
                            registration.discard_others()

        print "Final: S'han assignat un total de %d tallers" % count_assigned


