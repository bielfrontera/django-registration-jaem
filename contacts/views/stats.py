# coding: utf-8
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.db.models import Count
from django.template import RequestContext
from contacts.models import Person, CONTACT_TYPE_CHOICES, LANG_CHOICES, MATH_SOCIETY_CHOICES
from contacts.forms import StatsForm


import sys

def inscription(request,  template='contacts/person/stats.html'):
    """ Stats inscription
    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    stats_by = 'contact_type'
    if request.method == 'POST':
        form = StatsForm(request.POST)
        if form.is_valid():
            stats_by = form.cleaned_data['stats_by']
    else:
        form = StatsForm()

    inscription_stats = []
    if stats_by == 'contact_type':
        contact_types = dict(CONTACT_TYPE_CHOICES)
        for key  in contact_types.keys():
            regs = Person.objects.filter(contact_type=key).values('status').annotate(Count("id")).order_by()
            stat = {'contact_type': key,'contact_type_display': contact_types[key], 'regs' : regs  }
            inscription_stats.append(stat)
    elif stats_by == 'math_society':
        contact_types = dict(MATH_SOCIETY_CHOICES)
        for key  in contact_types.keys():
            regs = Person.objects.filter(math_society=key).values('status').annotate(Count("id")).order_by()
            stat = {'contact_type': key,'contact_type_display': contact_types[key], 'regs' : regs  }
            inscription_stats.append(stat)
    elif stats_by == 'lang':
        contact_types = dict(LANG_CHOICES)
        for key  in contact_types.keys():
            regs = Person.objects.filter(lang=key).values('status').annotate(Count("id")).order_by()
            stat = {'contact_type': key,'contact_type_display': contact_types[key], 'regs' : regs  }
            inscription_stats.append(stat)
    elif stats_by == 'province':
        provinces = set()
        for person in Person.objects.all():
            provinces.add(person.home_province)
        provinces = sorted(provinces)
        for key  in provinces:
            regs = Person.objects.filter(home_province=key).values('status').annotate(Count("id")).order_by()
            stat = {'contact_type': key,'contact_type_display': key, 'regs' : regs  }
            inscription_stats.append(stat)


    kwvars = {
        'inscription_stats' : inscription_stats,
        'form': form
    }

    return render_to_response(template, kwvars, RequestContext(request))



