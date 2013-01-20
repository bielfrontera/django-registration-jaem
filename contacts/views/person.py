# coding: utf-8

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.utils.html import escape
from datetime import date, datetime, timedelta
import csv

import MySQLdb
from django.conf import settings
from contacts.models import Person
from contacts.forms import PersonCreateForm, PersonUpdateForm, PersonFilterForm, ImportCSVForm, PersonIdentificationForm,PersonRegistrationForm, PersonAddressForm,                             PersonLaboralForm, SynchronizeSPIPForm, PersonLaboralLevelsForm
from contacts.tables import PersonTable, ExportPersonTable

import sys, ast


def check_pending_sync():
    lastperson = Person.objects.latest('external_id')
    db = MySQLdb.connect(host=settings.SPIP_DATABASE_HOST,user=settings.SPIP_DATABASE_USER,
                                     passwd=settings.SPIP_DATABASE_PASSWORD,db=settings.SPIP_DATABASE, charset='utf8')
    cur = db.cursor()
    cur.execute("""
        SELECT count(*) as regs_pending
        FROM spip_forms_donnees insc
        WHERE insc.id_donnee > %s
        AND insc.id_form = 1
    """ , lastperson.external_id )

    regs_pending = cur.fetchone()[0]

    # Close all cursors
    cur.close()
    # Close all databases
    db.close()

    return regs_pending

def list(request, page=1, template='contacts/person/list.html'):
    """List of all the people.

    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    person_list = Person.objects.all()

    if request.method == 'GET':
        form = PersonFilterForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['last_name']:
                person_list = person_list.filter(last_name__istartswith=form.cleaned_data['last_name'])

            if form.cleaned_data['id_card']:
                person_list = person_list.filter(id_card__istartswith=form.cleaned_data['id_card'])

            if form.cleaned_data['contact_type']:
                person_list = person_list.filter(contact_type=form.cleaned_data['contact_type'])

            if form.cleaned_data['status']:
                person_list = person_list.filter(status=form.cleaned_data['status'])

            if form.cleaned_data['mailnotpaid_unsent']:
                person_list = person_list.filter(date_mailnotpaid__isnull = True).exclude(status='ok_all')

            if form.cleaned_data['mailregister_unsent']:
                person_list = person_list.filter(date_mailregister__isnull = True, status='ok_all')

    else:
        form = PersonFilterForm()

    table = PersonTable(person_list, order_by = request.GET.get("sort",'-date_registration') )
    table.paginate(page=request.GET.get("page", 1))

    # Comprovam si hi ha nous registres per sincronitzar. Ho feim una vegada per sessio.
    if not request.session:
        request.session={}

    regs_not_sync = request.session.get('regs_not_sync',-1)
    if regs_not_sync == -1:
        regs_not_sync = check_pending_sync()
        request.session['regs_not_sync'] = regs_not_sync

    kwvars = {
        'table' : table,
        'form': form,
        'regs_not_sync': regs_not_sync,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def map(request, template='contacts/person/map.html'):
    """Map with google maps

    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    person_list = Person.objects.all()

    if request.method == 'POST':
        form = PersonFilterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['last_name']:
                person_list = person_list.filter(last_name__istartswith=form.cleaned_data['last_name'])

            if form.cleaned_data['id_card']:
                person_list = person_list.filter(id_card__istartswith=form.cleaned_data['id_card'])

            if form.cleaned_data['contact_type']:
                person_list = person_list.filter(contact_type=form.cleaned_data['contact_type'])

    else:
        form = PersonFilterForm()




    kwvars = {
        'person_list' : person_list,
        'form': form,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def export(request):
    """ Export people to csv
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    filename = 'export-inscrits%s.csv' % date.today().strftime("%y-%m-%d")

    person_list = Person.objects.all()

    table = ExportPersonTable(person_list)
    table.order_by = request.GET.get("sort",'last_name')

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    writer = csv.writer(response)
    # Write headers to CSV file
    headers = []
    for column in table.columns:
        headers.append(column.header.encode('utf8'))
    writer.writerow(headers)

    # Write data to CSV file
    for obj in table.rows:
        row = []
        for value in obj:
            row.append(value.encode('utf8'))
        writer.writerow(row)

    # Return CSV file to browser as download
    return response


def importCSV(request, template='contacts/person/import.html'):
    """ Import people from csv
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    registres = 0

    if request.method == 'POST':
        form = ImportCSVForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['fitxer']
            uploaded_file.read()
            reader = csv.reader(uploaded_file, delimiter=',', quotechar='"')

            for row in reader:
                person = Person()
                person.first_name = row[0]
                person.last_name = row[1]
                person.contact_type = row[3]
                person.id_card = row[5]

                base_slug = slugify("%s %s %s" % (p.first_name, p.last_name, p.secondlast_name))
                # hem de comprovar que no existeix cap persona amb aquest nom. Si no, hem d'afegir -1
                tmp_slug = base_slug
                trobat = True
                counter = 0

                while trobat:
                    try:
                        Person.objects.get(slug__iexact=tmp_slug)
                        counter = counter + 1
                        tmp_slug = "%s-%s" % (base_slug, str(counter))

                    except Person.DoesNotExist:
                        trobat = False

                person.slug = tmp_slug
                person.save()

                registres = registres + 1

    else:
        form = ImportCSVForm()

    return render_to_response(template, {'registres': registres, 'form': form}, RequestContext(request))

def calculaSlugPersona(person):
    base_slug = slugify("%s %s" % (person.first_name, person.last_name))
    # hem de comprovar que no existeix cap persona amb aquest nom. Si no, hem d'afegir -1
    tmp_slug = base_slug
    trobat = True
    counter = 0
    while trobat:
        try:
            Person.objects.get(slug__iexact=tmp_slug)
            counter = counter + 1
            tmp_slug = "%s-%s" % (base_slug, str(counter))
        except Person.DoesNotExist:
            trobat = False

    return tmp_slug

def synchronizeSPIPForm(request, template='contacts/person/synchronize.html'):
    """ Import inscriptions from spip form
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    registres = 0
    user = request.user

    if request.method == 'POST':
        form = SynchronizeSPIPForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['confirma'] == True:
                lastperson = Person.objects.latest('external_id')



                db = MySQLdb.connect(host=settings.SPIP_DATABASE_HOST,user=settings.SPIP_DATABASE_USER,
                                     passwd=settings.SPIP_DATABASE_PASSWORD,db=settings.SPIP_DATABASE, charset='utf8')
                cur = db.cursor()
                cur.execute("""
                    SELECT insc.id_donnee, insc.date, camp.champ, camp.valeur, valor.rang, valor.titre
                    FROM spip_forms_donnees insc, spip_forms_donnees_champs camp
                    LEFT OUTER JOIN spip_forms_champs_choix valor ON valor.champ = camp.champ
                    AND valor.choix = camp.valeur
                    WHERE insc.id_donnee = camp.id_donnee
                    AND insc.id_donnee > %s
                    AND insc.id_form = 1
                    AND insc.statut = 'publie'
                    ORDER BY insc.id_donnee, camp.champ
                """ % lastperson.external_id )

                person = Person()
                person.external_id = 0
                laboral_levels = []

                for row in cur.fetchall():
                    if row[0] != person.external_id and person.external_id > 0:
                        # donam d'alta la persona anterior
                        person.slug = calculaSlugPersona(person)
                        person.user_add = user
                        person.user_modify = user
                        person.save()
                        registres = registres + 1
                        # nova persona
                        person = Person()
                        laboral_levels = []

                    person.external_id = row[0]
                    person.date_registration = row[1]


                    if row[2] == 'ligne_1':
                        person.first_name = row[3] #.decode("utf8", "ignore")
                    elif row[2] == 'ligne_2':
                        person.last_name = row[3] #.decode("utf8", "ignore")
                    elif row[2] == 'ligne_3':
                        person.id_card = row[3]
                    elif row[2] == 'ligne_4':
                        person.home_address = row[3] #.decode("utf8", "ignore")
                    elif row[2] == 'ligne_5':
                        person.home_postalcode = row[3]
                    elif row[2] == 'ligne_6':
                        person.home_town = row[3] #.decode("utf8", "ignore")
                    elif row[2] == 'select_5':
                        person.home_province = row[5] #.decode("utf8", "ignore")
                    elif row[2] == 'email_1':
                        person.email_address = row[3]
                    elif row[2] == 'ligne_8':
                        person.phone_number = row[3]
                    elif row[2] == 'ligne_9':
                        person.mobile_number = row[3]
                    elif row[2] == 'ligne_19':
                        person.twitter = row[3] #.decode("utf8", "ignore")
                    elif row[2] == 'select_1':
                        person.laboral_category = row[4]
                    elif row[2] == 'multiple_1':
                        laboral_levels.append(row[4])
                        person.laboral_levels = ",".join("'%s'" % str(level)  for level in laboral_levels)
                        # print >> sys.stderr, 'Laboral levels = %s' % person.laboral_levels
                    elif row[2] == 'ligne_10':
                        person.laboral_nrp = row[3]
                    elif row[2] == 'num_1':
                        person.laboral_years = float(row[3]) if '.' in row[3] else int(row[3])
                    elif row[2] == 'select_2':
                        person.laboral_cuerpo = row[4]
                    elif row[2] == 'ligne_11':
                        person.laboral_degree = row[3] #.decode("utf8", "ignore")
                    elif row[2] == 'ligne_12':
                        person.laboral_centername = row[3] #.decode("utf8", "ignore")
                    elif row[2] == 'ligne_13':
                        person.laboral_centercode = row[3]
                    elif row[2] == 'ligne_16':
                        person.laboral_centerpostalcode = row[3]
                    elif row[2] == 'ligne_14':
                        person.laboral_centertown = row[3] #.decode("utf8", "ignore")
                    elif row[2] == 'select_4':
                        person.laboral_centerprovince = row[5] #.decode("utf8", "ignore")
                    elif row[2] == 'select_3':
                        person.math_society = row[4]
                    elif row[2] == 'texte_1':
                        person.remarks = row[3] #.decode("utf8", "ignore")
                    elif row[2] == 'select_6':
                        person.lang = row[4]



                # Hem de donar d'alta la darrera persona
                if person.external_id > 0:
                    person.slug = calculaSlugPersona(person)
                    person.user_add = user
                    person.user_modify = user
                    person.save()
                    registres = registres + 1

                # Close all cursors
                cur.close()
                # Close all databases
                db.close()
                # Posam a 0 els registres no sincronitzats
                if not request.session:
                    request.session={}
                request.session['regs_not_sync'] = 0

    else:
        form = SynchronizeSPIPForm()
        registres = -1

    return render_to_response(template, {'registres': registres, 'form': form}, RequestContext(request))


def detail(request, slug, template='contacts/person/detail.html'):
    """Detail of a person.

    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    try:
        person = Person.objects.get(slug__iexact=slug)

        if not request.session:
            request.session={}

        viewed_list = request.session.get('viewed',[])
        if person in viewed_list:
            viewed_list.remove(person)
        viewed_list.insert(0,person) # d'aquesta manera estara al final
        del viewed_list[8:10] # eliminam si hi ha moltes
        request.session['viewed'] = viewed_list

    except Person.DoesNotExist:
        raise Http404

    kwvars = {
        'object': person,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def create(request, template='contacts/person/create.html'):
    """Create a person.

    :param template: A custom template.

    https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#more-than-one-foreign-key-to-the-same-model
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('add_person'):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PersonCreateForm(request.POST)

        if form.is_valid():
            p = form.save(commit=False)
            base_slug = slugify("%s %s" % (p.first_name, p.last_name))

            # hem de comprovar que no existeix cap persona amb aquest nom. Si no, hem d'afegir -1
            tmp_slug = base_slug
            trobat = True
            counter = 0
            while trobat:
                try:
                    Person.objects.get(slug__iexact=tmp_slug)
                    counter = counter + 1
                    tmp_slug = "%s-%s" % (base_slug, str(counter))
                except Person.DoesNotExist:
                    trobat = False

            p.slug = tmp_slug
            p.user_add = user
            p.user_modify = user
            p.save()
            return HttpResponseRedirect(p.get_update_url())
    else:
        form = PersonCreateForm()

    kwvars = {
        'form': form
    }

    return render_to_response(template, kwvars, RequestContext(request))

def calculaStatus(person):
    if person.status == 'cancelled':
        return 'cancelled'

    status = 'pendent'
    if person.contact_type == 'R':
        if person.revision == 'dataok':
            if person.date_paid and person.paid:
                status = 'ok_all'
            else:
                status = 'ok_notpaid'
                # Revisam si fa molt de temps
                if (datetime.now() - person.date_registration).days > 15:
                    status = 'notpaid_late'
        else:
            if person.date_paid and person.paid:
                status = 'nook_paid'
            else:
                if (datetime.now() - person.date_registration).days > 15:
                    status = 'notpaid_late'
            # else (status = 'pendent')
    else:
        # son organitzadors, patrocinadors i convidats. Nomes necessitam data ok, no pagat
        if person.revision == 'dataok':
            status = 'ok_all'
    return status

def updateStatus(request,template='contacts/person/update_status.html'):
    """ Update status of pending records
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    person_list = Person.objects.filter(status__in = ['pendent','ok_notpaid'])
    registres = 0

    for person in person_list:
        status = calculaStatus(person)
        if status != person.status:
            person.status = status
            person.save()
            registres = registres + 1

    return render_to_response(template, {'registres': registres}, RequestContext(request))



def update(request, slug, template='contacts/person/update.html'):
    """Update a person.

    :param template: A custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('change_person'):
        #todo: posar al missatge que no es pot realitzar l'accio si no es te permis
        return detail(request,slug)
        # return HttpResponseForbidden()

    try:
        person = Person.objects.get(slug__iexact=slug)
    except Person.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        formId = PersonIdentificationForm(request.POST, instance=person)
        formReg = PersonRegistrationForm(request.POST, instance=person)
        formAdr = PersonAddressForm(request.POST, instance=person)
        formLab = PersonLaboralForm(request.POST, instance=person)
        formLevels = PersonLaboralLevelsForm(request.POST)

        # formLab.data['laboral_levels'] = [int(x) for x in formLab.data['laboral_levels']]

        if formId.is_valid() and formReg.is_valid() and formAdr.is_valid() and formLab.is_valid() and formLevels.is_valid():
            person.user_modify = user
            formId.save()
            formReg.save()
            formAdr.save()
            person.laboral_levels = formLevels.cleaned_data.get('laboral_levels')
            person.status = calculaStatus(person)
            formLab.save()

            return HttpResponseRedirect(person.get_absolute_url())

    else:
        formId = PersonIdentificationForm(instance=person)
        formReg = PersonRegistrationForm(instance=person)
        formAdr = PersonAddressForm(instance=person)
        formLab = PersonLaboralForm(instance=person)
        formLevels = PersonLaboralLevelsForm(initial={'laboral_levels': person.laboral_levels})
        # print >> sys.stderr, 'Laboral levels = %s' % person.laboral_levels

        # llista de persones consultades
        if not request.session:
            request.session={}
        viewed_list = request.session.get('viewed',[])
        if person in viewed_list:
            viewed_list.remove(person)
        viewed_list.insert(0,person) # d'aquesta manera estara al final
        del viewed_list[8:10] # eliminam si hi ha moltes
        request.session['viewed'] = viewed_list


    kwvars = {
        'id_form': formId,
        'reg_form': formReg,
        'adr_form': formAdr,
        'lab_form': formLab,
        'level_form': formLevels,
        'object': person,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def delete(request, slug, template='contacts/person/delete.html'):
    """Delete a person.

    :param template: A custom template.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('delete_person'):
        return HttpResponseForbidden()

    try:
        person = Person.objects.get(slug__iexact=slug)
    except Person.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        new_data = request.POST.copy()
        if new_data['delete_person'] == 'Yes':
            person.delete()
            return HttpResponseRedirect(reverse('contacts_person_list'))
        else:
            return HttpResponseRedirect(person.get_absolute_url())

    kwvars = {
        'object': person
    }

    return render_to_response(template, kwvars, RequestContext(request))

def cancel(request, slug, template='contacts/person/cancel.html'):
    """ Cancel a inscription // Or undo-cancel!

    :param template: A custom template.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('cancel_person'):
        return HttpResponseForbidden()

    try:
        person = Person.objects.get(slug__iexact=slug)
    except Person.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        new_data = request.POST.copy()
        if new_data['cancel_person'] == 'Yes':
            if person.status == 'cancelled':
                person.status = 'pendent'
                person.status = calculaStatus(person)
            else:
                person.status = 'cancelled'
            person.user_modify = user
            person.save()

        return HttpResponseRedirect(person.get_absolute_url())


    kwvars = {
        'object': person,
    }

    return render_to_response(template, kwvars, RequestContext(request))


def lookup(request):
    # Default return list
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'term'):
            value = request.GET[u'term']
            # Ignore queries shorter than length 3
            if len(value) > 2:
                model_results = Person.objects.filter(last_name__istartswith=value)
                results = [ {'label' : x.fullname, 'value': x.id } for x in model_results ]
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def revision(request, slug, template='contacts/person/revision.html'):
    """Delete a person.

    :param template: A custom template.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('revision_person'):
        return HttpResponseForbidden()

    try:
        person = Person.objects.get(slug__iexact=slug)
    except Person.DoesNotExist:
        raise Http404

    if request.method == 'POST':
            return HttpResponseRedirect(person.get_absolute_url())
    else:
        form = RevisionCreateForm()

    kwvars = {
        'object': person,
        'form': form
    }

    return render_to_response(template, kwvars, RequestContext(request))

