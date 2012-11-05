# coding: utf-8
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.db.models import Count
from django.template import RequestContext
from contacts.models import Person, CONTACT_TYPE_CHOICES

import sys

def inscription(request,  template='contacts/person/stats.html'):
    """ Stats inscription
    :param template: Add a custom template.
    """
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    # inscription_stats = Person.objects.values('contact_type').annotate(Count("id")).order_by()
    
    inscription_stats = []
    contact_types = dict(CONTACT_TYPE_CHOICES)
    for key  in contact_types.keys():        
        regs = Person.objects.filter(contact_type=key).values('status').annotate(Count("id")).order_by()
        stat = {'contact_type': key,'contact_type_display': contact_types[key], 'regs' : regs  }
        inscription_stats.append(stat)
            
    kwvars = {
        'inscription_stats' : inscription_stats,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def inscription_old(request,template='contacts/person/stats.html'):
    """ Stats inscription
    :param template: Add a custom template.
    """
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    inscription_stats = Person.objects.values('contact_type').annotate(Count("id")).order_by()
    
    inscription_stats2 = []
    for stat in inscription_stats:        
        stat2 = {'id__count': stat['id__count'] , 'contact_type':dict(CONTACT_TYPE_CHOICES)[stat['contact_type']] }
        inscription_stats2.append(stat2)
            
    kwvars = {
        'inscription_stats' : inscription_stats2,
    }

    return render_to_response(template, kwvars, RequestContext(request))

