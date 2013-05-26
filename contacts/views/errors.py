# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

import sys, traceback

def error500(request, template='contacts/errors/500.html'):
    """Show error

    :param template: Add a custom template.
    """
    ltype,lvalue,exc_traceback = sys.exc_info()
    ltraceback = traceback.format_tb(exc_traceback)

    kwvars = {
        'ltype': ltype,
        'lvalue': lvalue,
        'ltraceback': ltraceback,
    }

    return render_to_response(template, kwvars, RequestContext(request))