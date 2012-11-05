# coding: utf-8
from django.core.mail import EmailMessage
from django.http import Http404
from django.template import Template
from django.template.context import Context
from django.template.loader import get_template
from django.conf import settings
from contacts.models import MailTemplate
from django.utils.translation import ugettext as _


import os, sys
import StringIO
from xhtml2pdf import pisa


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path   
    
    
def sendTemplateMail(context,code,recipients):
    """
        SendMail from template.
    """    
    status = _('Mail not sent')
    try:
        mailtemplate = MailTemplate.objects.get(code__iexact=code)
    except MailTemplate.DoesNotExist:
        raise Http404
    subject = Template(mailtemplate.subject).render(context) 
    body = Template(mailtemplate.body).render(context)
    email = EmailMessage(subject, body, settings.EMAIL_FROM, recipients)
    
    if mailtemplate.attachment:
        template = "contacts/person/%s.html" % mailtemplate.attachment
        template = get_template(template)   
        html = template.render(context)
        result = StringIO.StringIO()    
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                                dest=result,
                                                encoding='UTF-8',
                                                link_callback=fetch_resources)
        if pdf.err:
            status = _('Error generating pdf')
            return status
        else:
            email.attach(mailtemplate.attachment, result.getvalue(), 'application/pdf')
    try:        
        email.send()
        status = _('Mail sent')
    except Exception as inst:   
        status = 'Error. Tipus: %s . Missatge: %s' % (type(inst) , inst)
    except:    
        status = _('Error sending mail')            
        
    return status
