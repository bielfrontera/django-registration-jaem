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
from contacts.forms import TallerRegistrationCreateForm, TallerRegistrationUpdateForm, TallerRegistrationFilterForm, TallerFilterForm
from contacts.tables import TallerRegistrationTable, ExportTallerRegistrationTable, TallerTable, ExportTallerTable
from django.utils.translation import ugettext as _

from contacts.functions.mailtemplate import sendTemplateMail

import sys, ast, random



def list(request, page=1, template='contacts/taller/list.html'):
    """List of all Tallers.

    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    taller_list = Taller.objects.all()

    if request.method == 'GET':
        form = TallerFilterForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['title']:
                taller_list = taller_list.filter(title__icontains=form.cleaned_data['title'])

            if form.cleaned_data['authors']:
                taller_list = taller_list.filter(authors__icontains=form.cleaned_data['authors'])

    else:
        form = TallerFilterForm()

    table = TallerTable(taller_list, order_by = request.GET.get("sort",'id') )
    table.paginate(page=request.GET.get("page", 1), per_page=30)

    kwvars = {
        'table' : table,
        'form': form,
    }

    return render_to_response(template, kwvars, RequestContext(request))


def export(request):
    """ Export tallers to csv
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    filename = 'export-tallers-%s.csv' % date.today().strftime("%y-%m-%d")

    regtaller_list = Taller.objects.all()

    table = ExportTallerTable(regtaller_list)
    table.order_by = request.GET.get("sort",'id')

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
            if isinstance(value, basestring):
                row.append(value.encode('utf8'))
            else:
                row.append(value)
        writer.writerow(row)

    # Return CSV file to browser as download
    return response

def detail(request, id, template='contacts/taller/detail.html'):
    """Detail of a taller registration.

    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    try:
        taller = Taller.objects.get(id=id)

    except TallerRegistration.DoesNotExist:
        raise Http404

    kwvars = {
        'object': taller,
    }

    return render_to_response(template, kwvars, RequestContext(request))
