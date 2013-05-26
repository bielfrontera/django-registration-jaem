# coding: utf-8
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.template.context import Context
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.utils import translation
from django.utils.html import escape
from datetime import date, datetime, timedelta
import csv
from django.conf import settings
from contacts.models import Excursion, Person
from contacts.forms import ExcursionCreateForm, ExcursionUpdateForm, ExcursionFilterForm
from contacts.tables import ExcursionTable, ExportExcursionTable
from django.utils.translation import ugettext as _

from contacts.functions.mailtemplate import sendTemplateMail

import sys, ast, random


def list(request, page=1, template='contacts/excursion/list.html'):
    """List of all the excursions.

    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    excursion_list = Excursion.objects.all()

    if request.method == 'GET':
        form = ExcursionFilterForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['last_name']:
                excursion_list = excursion_list.filter(last_name__istartswith=form.cleaned_data['last_name'])

            if form.cleaned_data['last_name']:
                excursion_list = excursion_list.filter(last_name__istartswith=form.cleaned_data['last_name'])

            if form.cleaned_data['status']:
                excursion_list = excursion_list.filter(status=form.cleaned_data['status'])

            if form.cleaned_data['mailnotpaid_unsent']:
                excursion_list = excursion_list.filter(date_mailnotpaid__isnull = True).exclude(status='ok_all')

            if form.cleaned_data['mailregister_unsent']:
                excursion_list = excursion_list.filter(date_mailregister__isnull = True, status='ok_all')

            if form.cleaned_data['email_address']:
                excursion_list = person_list.filter(email_address=form.cleaned_data['email_address'])
    else:
        form = ExcursionFilterForm()

    table = ExcursionTable(excursion_list, order_by = request.GET.get("sort",'-date_registration') )
    table.paginate(page=request.GET.get("page", 1))

    kwvars = {
        'table' : table,
        'form': form,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def export(request):
    """ Export excursions to csv
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    filename = 'export-excursio_sopar-%s.csv' % date.today().strftime("%y-%m-%d")

    excursion_list = Excursion.objects.all()

    table = ExportExcursionTable(excursion_list)
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


def detail(request, id, template='contacts/excursion/detail.html'):
    """Detail of a excursion.

    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    try:
        excursion = Excursion.objects.get(id=id)

    except Excursion.DoesNotExist:
        raise Http404

    kwvars = {
        'object': excursion,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def new(request, lang='session', template='contacts/excursion/new.html'):
    """Create a excursion.
    """

    if lang == 'session':
        if request.session:
            lang = request.session.get('lang','es')

    try:
        translation.activate(lang)
        request.LANGUAGE_CODE = translation.get_language()

        if not request.session:
            request.session={}
        request.session['lang'] = lang

    except:
        pass

    return create(request,template)

def create(request, template='contacts/excursion/create.html'):
    """Create a excursion.

    :param template: A custom template.
    """

    user = request.user

    if not user.is_authenticated():
        try:
            user = User.objects.get(first_name='Anonymous')
        except:
            username = str(random.randint(0,1000000))
            u = User(username=username, first_name='Anonymous', last_name='User')
            u.set_unusable_password()
            u.save()
            user = User.objects.get(first_name='Anonymous')

    if request.method == 'POST':
        form = ExcursionCreateForm(request.POST)

        if form.is_valid():
            p = form.save(commit=False)
            person_list = Person.objects.filter(email_address__iexact=p.email_address)
            person = None
            if person_list.count() > 0:
                for iter_person in person_list:
                    if person is None: person = iter_person
                    if iter_person.first_name.lower().strip() == p.first_name.lower().strip():
                        person = iter_person
                        break
            else:
                raise Exception( _("This email address doesn't exist in the inscription database"))

            p.person = person
            p.user_add = user
            p.user_modify = user
            p.date_registration = datetime.now()
            p.save()
            if user.is_authenticated() and user.first_name != 'Anonymous':
                return HttpResponseRedirect(p.get_update_url())
            else:
                # Enviam correu OK + Mostram success
                kwvars = {
                    'object': p
                }
                context = Context(kwvars)
                mailtemplate = 'exc_registration_es' if p.person.lang != '2' else 'exc_registration_ca'
                status = sendTemplateMail(context,mailtemplate,[p.email_address])
                if status == _('Mail sent'):
                    mail_ok = True
                else:
                    mail_ok = False

                return render_to_response('contacts/excursion/new_success.html', {'object': p, 'mail_ok' : mail_ok, 'mail_status': status}, RequestContext(request))

    else:
        form = ExcursionCreateForm()

    kwvars = {
        'form': form
    }

    return render_to_response(template, kwvars, RequestContext(request))

def calculaStatus(excursion):
    if excursion.status == 'cancelled':
        return 'cancelled'

    status = 'pendent'

    if excursion.date_paid:
        status = 'ok_all'
    else:
        status = 'pendent'
        # Revisam si fa molt de temps
        if (datetime.now() - excursion.date_registration).days > 15:
            status = 'notpaid_late'

    return status

def updateStatus(request,template='contacts/excursion/update_status.html'):
    """ Update status of pending records
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    excursion_list = Excursion.objects.filter(status__in = ['pendent','ok_notpaid'])
    registres = 0

    for excursion in excursion_list:
        status = calculaStatus(excursion)
        if status != excursion.status:
            excursion.status = status
            excursion.save()
            registres = registres + 1

    return render_to_response(template, {'registres': registres}, RequestContext(request))



def update(request, id, template='contacts/excursion/update.html'):
    """Update a excursion.

    :param template: A custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('change_excursion'):
        #todo: posar al missatge que no es pot realitzar l'accio si no es te permis
        return detail(request,slug)
        # return HttpResponseForbidden()

    try:
        excursion = Excursion.objects.get(id=id)
    except Excursion.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = ExcursionUpdateForm(request.POST, instance=excursion)


        if form.is_valid():
            excursion.user_modify = user
            excursion.status = calculaStatus(excursion)
            form.save()
            return HttpResponseRedirect(excursion.get_absolute_url())

    else:
        form = ExcursionUpdateForm(instance=excursion)

    kwvars = {
        'form': form,
        'object': excursion,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def delete(request, id, template='contacts/excursion/delete.html'):
    """Delete a excursion.

    :param template: A custom template.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('delete_excursion'):
        return HttpResponseForbidden()

    try:
        excursion = Excursion.objects.get(id=id)
    except Excursion.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        new_data = request.POST.copy()
        if new_data['delete_excursion'] == 'Yes':
            excursion.delete()
            return HttpResponseRedirect(reverse('contacts_excursion_list'))
        else:
            return HttpResponseRedirect(excursion.get_absolute_url())

    kwvars = {
        'object': excursion
    }

    return render_to_response(template, kwvars, RequestContext(request))

def cancel(request, id, template='contacts/excursion/cancel.html'):
    """ Cancel a inscription // Or undo-cancel!

    :param template: A custom template.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('cancel_excursion'):
        return HttpResponseForbidden()

    try:
        excursion = Excursion.objects.get(id=id)
    except Excursion.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        new_data = request.POST.copy()
        if new_data['cancel_excursion'] == 'Yes':
            if excursion.status == 'cancelled':
                excursion.status = 'pendent'
                excursion.status = calculaStatus(excursion)
            else:
                excursion.status = 'cancelled'
            excursion.user_modify = user
            excursion.save()

        return HttpResponseRedirect(excursion.get_absolute_url())


    kwvars = {
        'object': excursion,
    }

    return render_to_response(template, kwvars, RequestContext(request))
