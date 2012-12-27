# coding: utf-8
from django import template
from django.template.defaultfilters import stringfilter

from contacts.models import STATUS_CHOICES
from django.utils import translation

register = template.Library()

@register.filter
@stringfilter
def status_display(value):    
    return dict(STATUS_CHOICES)[value]
    
    
@register.filter
@stringfilter
def date_display_es(value):        
    cur_language = translation.get_language()
    try:
        translation.activate('es')
        text = translation.ugettext(value)
    finally:
        translation.activate(cur_language)
    return text