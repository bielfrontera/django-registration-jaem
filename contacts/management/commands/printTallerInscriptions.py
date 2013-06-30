# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand, make_option

from django.template.context import Context
from django.template.loader import render_to_string
from django.conf import settings
from contacts.models import Person, TallerRegistration, TallerRelation, Taller
from django.template.defaultfilters import slugify

import os



class Command(NoArgsCommand):

    help = "printTallerInscriptions"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )


    def handle_noargs(self, **options):
        taller_list = Taller.objects.all().order_by('day_scheduled','time_scheduled','building','room')

        file = open('public/contactes/img/inscrits_taller.svg')
        template_llistat = file.read()

        for taller in taller_list:
            print taller
            counter = 0
            page_number = 0

            new_page_llistat = template_llistat
            new_page_llistat = new_page_llistat.replace('%taller%', taller.title[0:65].encode('utf-8'))
            new_page_llistat = new_page_llistat.replace('%autors%', taller.authors[0:80].encode('utf-8'))
            datalloc = "Dia %s %s - %s. %s " % (taller.day_scheduled, taller.time_scheduled , taller.building, taller.room )
            new_page_llistat = new_page_llistat.replace('%datalloc%', datalloc.encode('utf-8'))
            new_page_llistat = new_page_llistat.replace('%max%', str(taller.max_attendants))



            people = []
            for relation in taller.attendants:
                people.append(relation.taller_registration.person)

            people = sorted(people, key=lambda person: person.last_name.lower())

            for person in people:
                name = "%s, %s" % (person.last_name, person.first_name)
                new_page_llistat = new_page_llistat.replace('%n' + str(counter % 21) + '%',str(counter+1))
                new_page_llistat = new_page_llistat.replace('%nom' + str(counter % 21) + '%',name.encode('utf-8'))

                counter = counter + 1

                if counter % 21 == 0:
                    save_llistat(new_page_llistat,str(taller),page_number)

                    page_number = page_number + 1

                    new_page_llistat = template_llistat
                    new_page_llistat = new_page_llistat.replace('%taller%', taller.title[0:65].encode('utf-8'))
                    new_page_llistat = new_page_llistat.replace('%autors%', taller.authors[0:80].encode('utf-8'))
                    datalloc = "Dia %s %s - %s. %s " % (taller.day_scheduled, taller.time_scheduled , taller.building, taller.room )
                    new_page_llistat = new_page_llistat.replace('%datalloc%', datalloc.encode('utf-8'))
                    new_page_llistat = new_page_llistat.replace('%max%', str(taller.max_attendants))

            if counter % 21 > 0:
                while counter % 21 > 0:
                    new_page_llistat = new_page_llistat.replace('%n' + str(counter % 21) + '%',str(counter+1))
                    new_page_llistat = new_page_llistat.replace('%nom' + str(counter % 21) + '%','')
                    counter = counter + 1

                save_llistat(new_page_llistat,str(taller),page_number)

def save_llistat(raw_svg,taller,page_number):
    filename = 'generated_files/tallers/' + slugify(taller) + str(page_number).zfill(3)
    with open( filename + '.svg', "wt") as out:
        out.write(raw_svg)
        out.close()
    # save as pdf
    os.system("inkscape -f %s.svg -A %s.pdf" % (filename, filename) )