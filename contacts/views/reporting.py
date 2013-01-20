# coding: utf-8
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.template import Template
from django.template.loader import get_template
from django.template.context import Context
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.utils import simplejson



from datetime import date, datetime
from django.conf import settings
from contacts.models import Person, MailTemplate

import os, sys
import StringIO
from xhtml2pdf import pisa

from contacts.functions.mailtemplate import sendTemplateMail

from django.utils import translation
from django.template.defaultfilters import date as _date

'''def fetch_resources(uri, rel):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))

        if not os.path.isfile(path):
            path = os.path.join(settings.MEDIA_ROOT,
                                uri.replace(settings.MEDIA_URL, ""))

            if not os.path.isfile(path):
                raise UnsupportedMediaPathException(
                                    'media urls must start with %s or %s' % (
                                    settings.MEDIA_ROOT, settings.STATIC_ROOT))

    return path'''

def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

def justificantPagament(request, slug,template='contacts/person/justificant_pagament_es.pdf.html' ):
    """
        Genera el pdf del justificant de Pagament a les JAEM
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user

    try:
        person = Person.objects.get(slug__iexact=slug)
    except Person.DoesNotExist:
        raise Http404

    # avui = datetime.today().strftime('%d de %B de %Y')
    avui = _date(datetime.now(), "d \d\e F \d\e Y")


    if person.lang == '1':
        cur_language = translation.get_language()
        try:
            translation.activate('es')
            avui = _date(datetime.now(), "d \d\e F \d\e Y")
        finally:
            translation.activate(cur_language)

    kwvars = {
        'object': person,
        'avui': avui
    }

    # revisam si la template ha de ser en catala
    if person.lang == '2':
        template = 'contacts/person/justificant_pagament_ca.pdf.html'


    template = get_template(template)
    context = Context(kwvars)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                            dest=result,
                                            encoding='UTF-8',
                                            link_callback=fetch_resources)
    if not pdf.err:
        response = HttpResponse(result.getvalue(),mimetype='application/pdf')
        return response

    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def mail(request,slug,code):
    """
        Envia i genera el pdf del justificant de Pagament a les JAEM
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    try:
        person = Person.objects.get(slug__iexact=slug)
    except Person.DoesNotExist:
        raise Http404

    avui = _date(datetime.now(), "d \d\e F \d\e Y")


    if person.lang == '1':
        cur_language = translation.get_language()
        try:
            translation.activate('es')
            avui = _date(datetime.now(), "d \d\e F \d\e Y")
        finally:
            translation.activate(cur_language)

    kwvars = {
        'object': person,
        'avui': avui
    }
    context = Context(kwvars)
    status = sendTemplateMail(context,code,[person.email_address])
    json = simplejson.dumps(status)
    return HttpResponse(json, mimetype='application/json')



def mailJustificantPagament(request,slug):
    """
        Envia i genera el pdf del justificant de Pagament a les JAEM
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    try:
        person = Person.objects.get(slug__iexact=slug)
    except Person.DoesNotExist:
        raise Http404

    avui = _date(datetime.now(), "d \d\e F \d\e Y")


    if person.lang == '1':
        cur_language = translation.get_language()
        try:
            translation.activate('es')
            avui = _date(datetime.now(), "d \d\e F \d\e Y")
        finally:
            translation.activate(cur_language)

    kwvars = {
        'object': person,
        'avui': avui
    }
    # ('R', _('Registrant')) -> justpagament
    # else (convidat, organitzacio, etc) -> justregistre
    if person.contact_type == 'R':
        if person.lang == '2':
            mailtemplate = 'justpagament_cat'
        else:
            mailtemplate = 'justpagament_esp'
    else:
        if person.lang == '2':
            mailtemplate = 'justregistre_cat'
        else:
            mailtemplate = 'justregistre_esp'

    context = Context(kwvars)
    status = sendTemplateMail(context,mailtemplate,[person.email_address])
    if status == _('Mail sent'):
        person.date_mailregister = datetime.now()
        person.save()

    json = simplejson.dumps(status)
    return HttpResponse(json, mimetype='application/json')

def mailPagamentRetrasat(request,slug):
    """
        Envia un mail avisant que el pagament de la inscripció de les JAEM no s'ha efectuat
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    try:
        person = Person.objects.get(slug__iexact=slug)
    except Person.DoesNotExist:
        raise Http404


    kwvars = {
        'object': person,
    }
    if person.lang == '2':
        mailtemplate = 'pagamentretrasat_cat'
    else:
        mailtemplate = 'pagamentretrasat_esp'

    context = Context(kwvars)
    status = sendTemplateMail(context,mailtemplate,[person.email_address])
    if status == _('Mail sent'):
        person.date_mailnotpaid = datetime.now()
        person.save()

    json = simplejson.dumps(status)
    return HttpResponse(json, mimetype='application/json')

def justificantRegistre(request, slug,template='contacts/person/justificant_registre_es.pdf.html' ):
    """
        Genera el pdf del justificant de Registre a les JAEM
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user

    try:
        person = Person.objects.get(slug__iexact=slug)
    except Person.DoesNotExist:
        raise Http404

    avui = _date(datetime.now(), "d \d\e F \d\e Y")

    if person.lang == '1':
        cur_language = translation.get_language()
        try:
            translation.activate('es')
            avui = _date(datetime.now(), "d \d\e F \d\e Y")
        finally:
            translation.activate(cur_language)

    kwvars = {
        'object': person,
        'avui': avui
    }

    # revisam si la template ha de ser en catala
    if person.lang == '2':
        template = 'contacts/person/justificant_registre_ca.pdf.html'


    template = get_template(template)
    context = Context(kwvars)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                            dest=result,
                                            encoding='UTF-8',
                                            link_callback=fetch_resources)
    if not pdf.err:
        response = HttpResponse(result.getvalue(),mimetype='application/pdf')
        return response

    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
