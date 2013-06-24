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
        person_list = person_list.exclude(status='cancelled')[:8]

        file = open('public/contactes/img/acreditacio.svg')
        template_acreditacio = file.read()


        for person in person_list:
            # generate barcode
            ean = barcode.get_barcode('ean', str(person.id).zfill(12))
            #save barcode
            filename = 'generated_files/acreditacions/barcode'
            ean.save(filename)
            # convert barcode svg in png
            os.system("inkscape -d 300 -z -f %s -j -a ""20:995:137:1020""  -e %s" % (filename + '.svg',filename + '.png'))
            filename = filename + '.png'
            # Rotate barcode
            os.system("convert -rotate 90 %s %s" % (filename, filename) )

            # generate acreditacio
            new_acreditacio = template_acreditacio.replace('___BARCODE___', os.getcwd() + '/' + filename)
            new_acreditacio = new_acreditacio.replace('%Nom%',person.first_name.encode('utf-8'))
            new_acreditacio = new_acreditacio.replace('%llinA%',person.last_name.encode('utf-8'))
            new_acreditacio = new_acreditacio.replace('%llinB%','')
            new_acreditacio = new_acreditacio.replace('%prov%',person.home_province.encode('utf-8'))


            acreditacio_filename = "generated_files/acreditacions/%s" % slugify("%s %s" % (person.last_name, person.first_name))
            with open(acreditacio_filename + '.svg', "wt") as out:
                out.write(new_acreditacio)
                out.close()
            # save as pdf
            os.system("inkscape -f %s.svg -A %s.pdf" % (acreditacio_filename, acreditacio_filename) )


