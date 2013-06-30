# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand, make_option

from django.template.context import Context
from django.template.loader import render_to_string
from django.conf import settings
from contacts.models import Person, Excursion
from django.template.defaultfilters import slugify

import os



class Command(NoArgsCommand):

    help = "printInscriptions"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )


    def handle_noargs(self, **options):
        person_list = Person.objects.all()
        person_list = person_list.exclude(status='cancelled')
        person_list = person_list.exclude(contact_type='V')
        person_list = person_list.exclude(contact_type='O')

        # people = sorted(person_list, key=lambda person: person.last_name.encode('utf-8').replace('Á','A').lower())

        file = open('public/contactes/img/llistat_inscrits.svg')
        template_llistat = file.read()
        counter = 0
        page_number = 1


        for person in person_list:
            print person.fullname

            if counter == 0:
                new_page_llistat = template_llistat
                new_page_llistat = new_page_llistat.replace('%PAGINA%', str(page_number))
                new_page_llistat = new_page_llistat.replace('%INICIAL%', uniupper(person.last_name.split()[0].encode('utf-8')))

            if person.status == 'ok_all':
                new_page_llistat = new_page_llistat.replace('%p' + str(counter) + '%','')
            else:
                new_page_llistat = new_page_llistat.replace('%p' + str(counter) + '%','P')

            name = "%s, %s" % (person.last_name, person.first_name)
            new_page_llistat = new_page_llistat.replace('%nom' + str(counter) + '%',uniupper(name[0:41].encode('utf-8')))

            # Search excursion
            if hasattr(person,'excursion'):
                if person.excursion.status != 'ok_all':
                    pendent = ' (P)'
                else:
                    pendent = ''
                new_page_llistat = new_page_llistat.replace('%e' + str(counter) + '%', str(person.excursion.qty_excursion) + pendent)
                new_page_llistat = new_page_llistat.replace('%s' + str(counter) + '%',str(person.excursion.qty_dinner) + pendent)
                new_page_llistat = new_page_llistat.replace('%b' + str(counter) + '%',str(person.excursion.qty_bus) + pendent)
            else:
                new_page_llistat = new_page_llistat.replace('%e' + str(counter) + '%','-')
                new_page_llistat = new_page_llistat.replace('%s' + str(counter) + '%','-')
                new_page_llistat = new_page_llistat.replace('%b' + str(counter) + '%','-')

            counter = counter + 1

            if person.last_name.upper().startswith('FUSTER') or person.last_name.upper().startswith('NOVO'):
                # new page.
                while counter < 27:
                    new_page_llistat = new_page_llistat.replace('%p' + str(counter) + '%','')
                    new_page_llistat = new_page_llistat.replace('%nom' + str(counter) + '%','')
                    new_page_llistat = new_page_llistat.replace('%e' + str(counter) + '%','')
                    new_page_llistat = new_page_llistat.replace('%s' + str(counter) + '%','')
                    new_page_llistat = new_page_llistat.replace('%b' + str(counter) + '%','')
                    counter = counter + 1



            if counter == 27:
                new_page_llistat = new_page_llistat.replace('%FINAL%', uniupper(person.last_name.split()[0].encode('utf-8')))
                save_llistat(new_page_llistat,page_number)
                page_number = page_number + 1
                counter = 0

        if counter > 0:
            new_page_llistat = new_page_llistat.replace('%FINAL%', 'ZURITA')
            while counter < 27:
                new_page_llistat = new_page_llistat.replace('%p' + str(counter) + '%','')
                new_page_llistat = new_page_llistat.replace('%nom' + str(counter) + '%','')
                new_page_llistat = new_page_llistat.replace('%e' + str(counter) + '%','')
                new_page_llistat = new_page_llistat.replace('%s' + str(counter) + '%','')
                new_page_llistat = new_page_llistat.replace('%b' + str(counter) + '%','')
                counter = counter + 1
            save_llistat(new_page_llistat,page_number)

def save_llistat(raw_svg,page_number):
    filename = 'generated_files/inscripcions/llistat_inscripcions_pag' +  str(page_number).zfill(3)
    with open( filename + '.svg', "wt") as out:
        out.write(raw_svg)
        out.close()
    # save as pdf
    os.system("inkscape -f %s.svg -A %s.pdf" % (filename, filename) )

def uniupper(s):
    s = s.upper()
    s = s.replace('á','Á').replace('é','É').replace('í','Í').replace('ó','Ó').replace('ú','Ú')
    s = s.replace('ü','Ü').replace('ï','Ï')
    s = s.replace('à','À').replace('è','È').replace('ò','Ò')
    s = s.replace('ç','Ç').replace('ñ','Ñ')
    return s