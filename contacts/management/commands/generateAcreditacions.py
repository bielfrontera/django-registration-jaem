from django.core.management.base import NoArgsCommand, make_option

from django.template.context import Context
from django.template.loader import render_to_string
from django.conf import settings
from contacts.models import Person
from django.template.defaultfilters import slugify


import StringIO, os, barcode



class Command(NoArgsCommand):

    help = ""

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )


    def handle_noargs(self, **options):
        person_list = Person.objects.all()
        person_list = person_list.exclude(status='cancelled')
        # person_list = person_list.exclude(contact_type='V')
        person_list = person_list.filter(contact_type='V').order_by('last_name', 'first_name')

        file = open('public/contactes/img/9_acreditacions_voluntaris.svg')
        template_acreditacio = file.read()

        counter = 0
        page_number = 0
        new_acreditacio = template_acreditacio
        for person in person_list:
            # generate barcode
            ean = barcode.get_barcode('ean', str(person.id).zfill(12))
            #save barcode
            filename = 'generated_files/acreditacions/barcode'
            ean.save(filename)
            # convert barcode svg in png
            os.system("inkscape -d 300 -z -f %s -j -a ""20:995:137:1020""  -e %s" % (filename + '.svg',filename + str(counter) + '.png'))
            filename = filename + str(counter) + '.png'
            # Rotate barcode
            os.system("convert -rotate 90 %s %s" % (filename, filename) )

            # generate acreditacio
            new_acreditacio = new_acreditacio.replace('%codibarres' + str(counter) + '%', os.getcwd() + '/' + filename)
            new_acreditacio = new_acreditacio.replace('%nom' + str(counter) + '%',person.first_name.encode('utf-8'))
            new_acreditacio = new_acreditacio.replace('%llinatges' + str(counter) + '%',person.last_name.encode('utf-8'))
            new_acreditacio = new_acreditacio.replace('%lloc' + str(counter) + '%',person.home_province.encode('utf-8'))
            print "%d - %s - Pos %d" % (person.id, person.fullname, counter)

            counter = counter + 1

            if counter == 9:
                save_acreditacions(new_acreditacio,page_number)
                new_acreditacio = template_acreditacio
                page_number = page_number + 1
                counter = 0

        if counter > 0:
            while counter < 9:
                new_acreditacio = new_acreditacio.replace('%codibarres' + str(counter) + '%', os.getcwd() + '/generated_files/acreditacions/emptybarcode.png')
                new_acreditacio = new_acreditacio.replace('%nom' + str(counter) + '%','')
                new_acreditacio = new_acreditacio.replace('%llinatges' + str(counter) + '%','')
                new_acreditacio = new_acreditacio.replace('%lloc' + str(counter) + '%','')
                counter = counter +1

            save_acreditacions(new_acreditacio,page_number)



def save_acreditacions(raw_svg,page_number):
    acreditacio_filename = 'generated_files/acreditacions/acreditacions_voluntaris_pag' + str(page_number).zfill(3)
    with open( acreditacio_filename + '.svg', "wt") as out:
        out.write(raw_svg)
        out.close()
    # save as pdf
    os.system("inkscape -f %s.svg -A %s.pdf" % (acreditacio_filename, acreditacio_filename) )

