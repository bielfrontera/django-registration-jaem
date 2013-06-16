# coding: utf-8
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.template.context import Context
from django.utils import translation
from django.utils.html import escape
from datetime import date, datetime, timedelta
import csv
from django.conf import settings
from contacts.models import TallerRelation, Taller, TallerRegistration, Person
from contacts.forms import TallerRegistrationCreateForm, TallerRegistrationUpdateForm, TallerRegistrationFilterForm
from contacts.tables import TallerRegistrationTable, ExportTallerRegistrationTable
from django.utils.translation import ugettext as _

from contacts.functions.mailtemplate import sendTemplateMail

import sys, ast, random


def list(request, page=1, template='contacts/regtaller/list.html'):
    """List of all the Taller Registrations.

    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    regtaller_list = TallerRegistration.objects.all()

    if request.method == 'GET':
        form = TallerRegistrationFilterForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['last_name']:
                regtaller_list = regtaller_list.filter(last_name__istartswith=form.cleaned_data['last_name'])

            if form.cleaned_data['email_address']:
                regtaller_list = person_list.filter(email_address=form.cleaned_data['email_address'])
    else:
        form = TallerRegistrationFilterForm()

    table = TallerRegistrationTable(regtaller_list, order_by = request.GET.get("sort",'-date_registration') )
    table.paginate(page=request.GET.get("page", 1))

    kwvars = {
        'table' : table,
        'form': form,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def export(request):
    """ Export tallerRegistrations to csv
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    filename = 'export-inscripcions-tallers-%s.csv' % date.today().strftime("%y-%m-%d")

    regtaller_list = TallerRegistration.objects.all()

    table = ExportTallerRegistrationTable(regtaller_list)
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


def detail(request, id, template='contacts/regtaller/detail.html'):
    """Detail of a taller registration.

    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    try:
        regtaller = TallerRegistration.objects.get(id=id)

    except TallerRegistration.DoesNotExist:
        raise Http404

    kwvars = {
        'object': regtaller,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def new(request, lang='session', template='contacts/regtaller/new.html'):
    """Create a taller registration.
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

def create(request, template='contacts/regtaller/create.html'):
    """Create a taller registration.

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
        form = TallerRegistrationCreateForm(request.POST)


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
            # delete previous registration
            try:
                regtaller = TallerRegistration.objects.get(person_id__exact=person.id)
                regtaller.delete()
            except TallerRegistration.DoesNotExist:
                pass

            p.user_add = user
            p.user_modify = user
            p.date_registration = datetime.now()
            p.save()

            # tallers
            order = 0
            for taller_id in form.cleaned_data['tallers'].split(','):
                order = order + 1
                trelation = TallerRelation(taller_id=taller_id, taller_registration_id=p.id,preference_order=order)
                trelation.save()

            if user.is_authenticated() and user.first_name != 'Anonymous':
                return HttpResponseRedirect(p.get_absolute_url())
            else:
                # Enviam correu OK + Mostram success
                kwvars = {
                    'object': p
                }
                context = Context(kwvars)
                mailtemplate = 'tll_registration_es' if p.person.lang != '2' else 'tll_registration_ca'
                status = sendTemplateMail(context,mailtemplate,[p.email_address])
                if status == _('Mail sent'):
                    mail_ok = True
                else:
                    mail_ok = False

                return render_to_response('contacts/regtaller/new_success.html', {'object': p, 'mail_ok' : mail_ok, 'mail_status': status}, RequestContext(request))

    else:
        form = TallerRegistrationCreateForm()

    kwvars = {
        'form': form
    }

    return render_to_response(template, kwvars, RequestContext(request))


def update(request, id, template='contacts/regtaller/update.html'):
    """Update a taller registration.

    :param template: A custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('change_regtaller'):
        #todo: posar al missatge que no es pot realitzar l'accio si no es te permis
        return detail(request,slug)
        # return HttpResponseForbidden()

    try:
        regtaller = TallerRegistration.objects.get(id=id)
    except TallerRegistration.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = TallerRegistrationUpdateForm(request.POST, instance=regtaller)


        if form.is_valid():
            regtaller.user_modify = user
            form.save()
            return HttpResponseRedirect(regtaller.get_absolute_url())

    else:
        form = TallerRegistrationUpdateForm(instance=regtaller)

    kwvars = {
        'form': form,
        'object': regtaller,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def delete(request, id, template='contacts/regtaller/delete.html'):
    """Delete a taller registration.

    :param template: A custom template.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('delete_regtaller'):
        return HttpResponseForbidden()

    try:
        regtaller = TallerRegistration.objects.get(id=id)
    except TallerRegistration.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        new_data = request.POST.copy()
        if new_data['delete_regtaller'] == 'Yes':
            regtaller.delete()
            return HttpResponseRedirect(reverse('contacts_regtaller_list'))
        else:
            return HttpResponseRedirect(regtaller.get_absolute_url())

    kwvars = {
        'object': regtaller
    }

    return render_to_response(template, kwvars, RequestContext(request))

