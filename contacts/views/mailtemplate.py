# coding: utf-8

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.utils.html import escape
from contacts.models import MailTemplate
from contacts.forms import MailTemplateForm 
from contacts.tables import MailTemplateTable
from django.utils import simplejson

from copy import deepcopy

def list(request, page=1, template='contacts/mailtemplate/list.html'):
    """List of all the mailtemplates

    :param template: Add a custom template.
    """
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    mailtemplate_list = MailTemplate.objects.all()
            
    table = MailTemplateTable(mailtemplate_list, order_by = request.GET.get("sort",'code') )
    table.paginate(page=request.GET.get("page", 1))
    
    kwvars = {
        'table' : table
    }

    return render_to_response(template, kwvars, RequestContext(request))
    
def detail(request, code, template='contacts/mailtemplate/detail.html'):
    """Detail of a mailtemplate.

    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
        
    try:
        mailtemplate = MailTemplate.objects.get(code__iexact=code)
    except MailTemplate.DoesNotExist:
        raise Http404

    kwvars = {
        'object': mailtemplate,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def copy(request, code, template='contacts/mailtemplate/create.html'):
    """Copia una mailtemplate.

    :param template: Add a custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
        
    user = request.user    
    if not user.has_perm('add_mailtemplate'):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = MailTemplateForm(request.POST)

        if form.is_valid():
            p = form.save(commit=False)            
            p.user_add = user
            p.user_modify = user  
            p.save()
            return HttpResponseRedirect(p.get_update_url())
    else:
        try:
            mailtemplate = MailTemplate.objects.get(code__iexact=code)
        except MailTemplate.DoesNotExist:
            raise Http404
        
        new_mailtemplate = deepcopy(mailtemplate)
        new_mailtemplate.id = None
        new_mailtemplate.code = "%s_cp" % mailtemplate.code
        
        form = MailTemplateForm(instance=new_mailtemplate)
    
    kwvars = {
        'form': form,
    }

    return render_to_response(template, kwvars, RequestContext(request))

    
def create(request, template='contacts/mailtemplate/create.html'):
    """Create a mailtemplate.

    :param template: A custom template.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
        
    user = request.user
    if not user.has_perm('add_mailtemplate'):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = MailTemplateForm(request.POST)

        if form.is_valid():
            p = form.save(commit=False)            
            p.user_add = user
            p.user_modify = user  
            p.save()
            return HttpResponseRedirect(p.get_update_url())
    else:
        form = MailTemplateForm()

    kwvars = {
        'form': form
    }

    return render_to_response(template, kwvars, RequestContext(request))
    
    
def update(request, code, template='contacts/mailtemplate/update.html'):
    """Update a mailtemplate.

    :param template: A custom template.
    """
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('change_mailtemplate'):
        #todo: posar al missatge que no es pot realitzar l'accio si no es te permis
        return detail(request,code)
        
    try:
        mailtemplate = MailTemplate.objects.get(code__iexact=code)
    except MailTemplate.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = MailTemplateForm(request.POST, instance=mailtemplate)
        
        if form.is_valid():            
            mailtemplate.user_modify = user              
            form.save()
            return HttpResponseRedirect(mailtemplate.get_absolute_url())            
    else:
        form = MailTemplateForm(instance=mailtemplate)

    kwvars = {
        'form': form,
        'object': mailtemplate,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def delete(request, code, template='contacts/mailtemplate/delete.html'):
    """Delete a mailtemplate.

    :param template: A custom template.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    user = request.user
    if not user.has_perm('delete_mailtemplate'):
        return HttpResponseForbidden()

    try:
        mailtemplate = MailTemplate.objects.get(code__iexact=code)
    except MailTemplate.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        new_data = request.POST.copy()
        if new_data['delete_mailtemplate'] == 'Yes':
            mailtemplate.delete()
            return HttpResponseRedirect(reverse('contacts_mailtemplate_list'))
        else:
            return HttpResponseRedirect(mailtemplate.get_absolute_url())

    kwvars = {
        'object': mailtemplate
    }

    return render_to_response(template, kwvars, RequestContext(request))
   
def lookup(request):
    # Default return list
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'term'):
            value = request.GET[u'term']
            model_results = MailTemplate.objects.filter(code__istartswith=value)                
        else:
            model_results = MailTemplate.objects.all()                
        results = [ {'label' : x.subject, 'value': x.code } for x in model_results ]    
                
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

